CREATE TABLE IF NOT EXISTS reports (
  id BIGINT PRIMARY KEY,
  employee_name TEXT NOT NULL,
  employee_id TEXT NOT NULL,
  problem TEXT NOT NULL,
  location TEXT,
  created_at TIMESTAMPTZ NOT NULL
);

-- Safe to re-run against an already-initialized database (fresh volumes get this via CREATE TABLE above).
ALTER TABLE reports ADD COLUMN IF NOT EXISTS location TEXT;

-- Data migrated from the old reports.json file store.
INSERT INTO reports (id, employee_name, employee_id, problem, created_at) VALUES
  (1784480442303, 'Test Employee', 'E999', 'Overenie perzistencie po reštarte', '2026-07-19T17:00:42.303Z'),
  (1784480571942, 'Jozo', '345', 'padol srobovak', '2026-07-19T17:02:51.942Z'),
  (1784480922541, 'Fero', '453', 'problem xxx', '2026-07-19T17:08:42.541Z'),
  (1784481156116, 'Jana Nováková', 'EMP-001', 'Tlačiareň v kancelárii nefunguje.', '2026-07-19T17:12:36.116Z'),
  (1784481156119, 'Jana Nováková', 'EMP-001', 'Tlačiareň v kancelárii nefunguje.', '2026-07-19T17:12:36.119Z'),
  (1784481159297, 'Peter Testovací', 'EMP-999', 'Formulár neodosiela dáta.', '2026-07-19T17:12:39.297Z'),
  (1784481159590, 'Peter Testovací', 'EMP-999', 'Formulár neodosiela dáta.', '2026-07-19T17:12:39.590Z')
ON CONFLICT (id) DO NOTHING;
