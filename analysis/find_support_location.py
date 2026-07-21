"""
Navrhne mesto na Slovensku, kde umiestniť podporného pracovníka riešiaceho
nahlásené problémy (tabuľka `reports`), tak aby boli celkové výjazdové
náklady (najazdené km vážené počtom reportov z danej lokality) čo najnižšie.

Postup:
1. Pripojí sa priamo na Postgres a spočíta reporty podľa lokality.
2. Každej lokalite priradí súradnice (LOCATION_COORDS nižšie).
3. sklearn.cluster.KMeans(n_clusters=1) so sample_weight=počet reportov
   nájde vážené "ťažisko" všetkých hlásených problémov.
4. sklearn.neighbors.NearestNeighbors nájde najbližšie reálne mesto
   z kandidátov (CANDIDATE_CITIES) k tomuto ťažisku — support človek totiž
   musí sídliť v reálnom meste, nie v bode uprostred poľa.
5. Vypíše odporúčanie a porovnanie s pár zjavnými alternatívami.

Spustenie:
    pip install -r requirements.txt
    PGHOST=localhost PGPORT=5433 PGUSER=expense_tracker \
    PGPASSWORD=expense_tracker PGDATABASE=expense_tracker \
    python find_support_location.py
"""

import os

import numpy as np
import psycopg2
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

# Približné súradnice (lat, lon) lokalít vyskytujúcich sa v testovacích dátach.
LOCATION_COORDS = {
    # veľké mestá
    "Bratislava": (48.1486, 17.1077),
    "Košice": (48.7164, 21.2611),
    "Prešov": (48.9982, 21.2393),
    "Žilina": (49.2231, 18.7397),
    "Nitra": (48.3081, 18.0827),
    "Banská Bystrica": (48.7395, 19.1535),
    "Trnava": (48.3709, 17.5886),
    # stredné mestá
    "Poprad": (49.0553, 20.2969),
    "Martin": (49.0651, 18.9219),
    "Trenčín": (48.8945, 18.0444),
    "Prievidza": (48.7712, 18.6272),
    "Zvolen": (48.5763, 19.1227),
    "Michalovce": (48.7558, 21.9189),
    "Spišská Nová Ves": (48.9445, 20.5673),
    "Komárno": (47.7633, 18.1258),
    "Levice": (48.2135, 18.6066),
    "Humenné": (48.9358, 21.9111),
    "Bardejov": (49.2939, 21.2739),
    "Liptovský Mikuláš": (49.0821, 19.6119),
    "Ružomberok": (49.0763, 19.3084),
    "Piešťany": (48.5910, 17.8256),
    # obce/dediny
    "Príbovce": (49.1339, 18.8069),
    "Necpaly": (49.0932, 18.8556),
    "Blatnica": (49.0710, 18.9440),
    "Folkušová": (49.0480, 19.3560),
    "Turčianske Jaseno": (49.0100, 19.2350),
    "Slovenské Pravno": (48.9440, 18.6420),
    "Diviaky nad Nitricou": (48.7480, 18.4970),
    "Oravská Lesná": (49.3660, 19.1690),
    "Zákamenné": (49.3690, 19.3150),
    "Klin": (49.3760, 19.4090),
    "Mútne": (49.4110, 19.4090),
    "Rabča": (49.4450, 19.4460),
    "Sihelné": (49.4130, 19.4890),
    "Krivá": (49.3070, 19.3220),
    "Liesek": (49.3620, 19.5140),
    "Vitanová": (49.3860, 19.5390),
    "Nižná": (49.2960, 19.5590),
    "Vyšný Kubín": (49.2210, 19.3200),
    "Jasenová": (49.2280, 19.3010),
    "Malatiná": (49.2400, 19.2660),
    "Zázrivá": (49.2650, 19.1670),
    "Terchová": (49.2600, 19.0080),
    "Nová Bystrica": (49.3660, 18.9860),
    "Stará Bystrica": (49.3440, 18.9560),
    "Turzovka": (49.4020, 18.6210),
    "Makov": (49.4020, 18.4890),
    "Podvysoká": (49.4370, 18.5650),
    "Vysoká nad Kysucou": (49.4470, 18.6600),
    "Oščadnica": (49.4090, 18.9010),
}

# Kandidáti na umiestnenie podpory: reálne mestá s dobrou dopravnou dostupnosťou
# (okresné/krajské mestá). Podmnožina LOCATION_COORDS bez malých obcí.
CANDIDATE_CITIES = {
    name: coords
    for name, coords in LOCATION_COORDS.items()
    if name
    in {
        "Bratislava", "Košice", "Prešov", "Žilina", "Nitra", "Banská Bystrica",
        "Trnava", "Poprad", "Martin", "Trenčín", "Prievidza", "Zvolen",
        "Michalovce", "Spišská Nová Ves", "Komárno", "Levice", "Humenné",
        "Bardejov", "Liptovský Mikuláš", "Ružomberok", "Piešťany",
    }
}


def fetch_report_counts():
    conn = psycopg2.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5433"),
        user=os.environ.get("PGUSER", "expense_tracker"),
        password=os.environ.get("PGPASSWORD", "expense_tracker"),
        dbname=os.environ.get("PGDATABASE", "expense_tracker"),
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT location, COUNT(*)
                FROM reports
                WHERE location IS NOT NULL AND location <> ''
                GROUP BY location
                """
            )
            return cur.fetchall()
    finally:
        conn.close()


def project(lat, lon, lat0):
    """Equirectangular projection to km — dostatočne presné na rozlohu Slovenska."""
    r = 6371.0
    x = np.radians(lon) * np.cos(np.radians(lat0)) * r
    y = np.radians(lat) * r
    return x, y


def main():
    rows = fetch_report_counts()

    known = [(loc, cnt) for loc, cnt in rows if loc in LOCATION_COORDS]
    unknown = [loc for loc, _ in rows if loc not in LOCATION_COORDS]
    if unknown:
        print(f"Pozor: {len(unknown)} lokalít nemá priradené súradnice, vynechávam: {unknown}\n")

    if not known:
        print("Žiadne rozpoznané lokality v databáze.")
        return

    lats = np.array([LOCATION_COORDS[loc][0] for loc, _ in known])
    lons = np.array([LOCATION_COORDS[loc][1] for loc, _ in known])
    weights = np.array([cnt for _, cnt in known], dtype=float)
    lat0 = lats.mean()

    xs, ys = project(lats, lons, lat0)
    points = np.column_stack([xs, ys])

    kmeans = KMeans(n_clusters=1, n_init=10, random_state=42)
    kmeans.fit(points, sample_weight=weights)
    center = kmeans.cluster_centers_[0]

    cand_names = list(CANDIDATE_CITIES.keys())
    cand_lats = np.array([CANDIDATE_CITIES[n][0] for n in cand_names])
    cand_lons = np.array([CANDIDATE_CITIES[n][1] for n in cand_names])
    cand_x, cand_y = project(cand_lats, cand_lons, lat0)
    cand_points = np.column_stack([cand_x, cand_y])

    nn = NearestNeighbors(n_neighbors=1).fit(cand_points)
    dist, idx = nn.kneighbors([center])
    best_city = cand_names[idx[0][0]]

    def total_weighted_distance(city_name):
        clat, clon = CANDIDATE_CITIES[city_name]
        cx, cy = project(np.array([clat]), np.array([clon]), lat0)
        d = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
        return float(np.sum(d * weights))

    print("=== Počet reportov podľa lokality (top 10) ===")
    for loc, cnt in sorted(known, key=lambda r: -r[1])[:10]:
        print(f"  {loc:<25} {cnt}")

    print(f"\nOdporúčané mesto pre umiestnenie podpory: {best_city}")
    print(f"Vzdialenosť váženého ťažiska reportov od {best_city}: {dist[0][0]:.1f} km\n")

    print("=== Celková vážená vzdialenosť (súčet: počet_reportov × km) pre kandidátov ===")
    comparison_cities = sorted(
        {best_city, "Bratislava", "Žilina", "Banská Bystrica", "Košice"}
    )
    for city in sorted(comparison_cities, key=total_weighted_distance):
        marker = "  <-- odporúčané" if city == best_city else ""
        print(f"  {city:<20} {total_weighted_distance(city):>12,.0f} km-reportov{marker}")


if __name__ == "__main__":
    main()
