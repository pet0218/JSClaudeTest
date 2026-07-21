"""
Prejde všetky popisy problémov v tabuľke `reports` a cez Claude API
navrhne top 5 nástrojov/zariadení, do ktorých by sa firme oplatilo
investovať, aby vyriešila najviac nahlásených problémov.

Na rozdiel od find_support_location.py (štatistická optimalizácia
polohy) tu ide o sémantickú úlohu — pochopiť OBSAH voľného textu
naprieč stovkami hlásení a nájsť príčinové vzory. To sklearn/štatistika
bez LLM nevie: text je v prirodzenom jazyku, kategórie nie sú vopred
dané a rôzne formulácie (traktor/kosačka/hydraulika/dodávka) treba
sémanticky zoskupiť pod spoločné príčiny predtým, než sa dá odporučiť
investícia.

Spustenie:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=...
    PGHOST=localhost PGPORT=5433 PGUSER=expense_tracker \
    PGPASSWORD=expense_tracker PGDATABASE=expense_tracker \
    python suggest_investments_llm.py
"""

import os

import anthropic
import psycopg2


def fetch_reports():
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
                SELECT id, location, problem
                FROM reports
                WHERE problem IS NOT NULL AND problem <> ''
                ORDER BY id
                """
            )
            return cur.fetchall()
    finally:
        conn.close()


def build_prompt(rows):
    lines = []
    for report_id, location, problem in rows:
        loc = location or "neznáma lokalita"
        lines.append(f"[{report_id}] ({loc}) {problem}")
    joined = "\n".join(lines)

    return f"""Nasleduje {len(rows)} hlásení problémov od zamestnancov firmy,
každé vo formáte "[id] (lokalita) popis problému".

{joined}

Over si sekvenčne obsah všetkých hlásení vyššie a urob nasledovné:

1. Identifikuj hlavné opakujúce sa príčiny/kategórie problémov, ktoré v dátach vidíš
   (napr. konkrétny typ zariadenia, infraštruktúry alebo procesu, ktorý zlyháva
   opakovane).
2. Navrhni TOP 5 konkrétnych nástrojov/zariadení/investícií, do ktorých by sa firme
   oplatilo investovať, aby pokryla čo najviac týchto problémov naraz. Zoraď ich
   podľa očakávaného dopadu (koľko hlásení by daná investícia adresovala).
3. Pre každú z top 5 investícií uveď:
   - názov investície
   - približný počet/podiel hlásení, ktoré by riešila (s odkazom na typické id, nie
     nutne všetky)
   - stručné odôvodnenie (1-2 vety)
4. Na záver pridaj krátky odsek s celkovým zhrnutím zistených vzorov (napr. súvis
   medzi typom lokality a typom problému, ak ho vidíš).

Odpovedz v slovenčine, vecne a stručne, vo forme štruktúrovaného zoznamu."""


def main():
    rows = fetch_reports()
    print(f"Načítaných {len(rows)} hlásení z databázy.\n")

    prompt = build_prompt(rows)

    client = anthropic.Anthropic()

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=8000,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        final = stream.get_final_message()

    print("\n\n---")
    print(
        f"Tokeny: input={final.usage.input_tokens}, "
        f"output={final.usage.output_tokens}"
    )


if __name__ == "__main__":
    main()
