import express from "express";
import cors from "cors";
import pg from "pg";
import { initialTransactions } from "./src/data/transactions.js";

// Return BIGINT columns as JS numbers instead of strings.
pg.types.setTypeParser(20, (val) => parseInt(val, 10));

const pool = new pg.Pool();

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

const REPORTS_SELECT = `
  SELECT id, employee_name AS "employeeName", employee_id AS "employeeId", problem, location, created_at AS "createdAt"
  FROM reports
`;

app.get("/api/transactions", (req, res) => {
  res.json(initialTransactions);
});

app.get("/api/reports", async (req, res) => {
  const { rows } = await pool.query(`${REPORTS_SELECT} ORDER BY created_at ASC`);
  res.json(rows);
});

app.post("/api/reports", async (req, res) => {
  const { employeeName, employeeId, problem, location } = req.body;

  if (!employeeName || !employeeId || !problem || !location) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  const { rows } = await pool.query(
    `INSERT INTO reports (id, employee_name, employee_id, problem, location, created_at)
     VALUES ($1, $2, $3, $4, $5, $6)
     RETURNING id, employee_name AS "employeeName", employee_id AS "employeeId", problem, location, created_at AS "createdAt"`,
    [Date.now(), employeeName, employeeId, problem, location, new Date()]
  );

  res.status(201).json(rows[0]);
});

app.listen(PORT, () => {
  console.log(`API server running at http://localhost:${PORT}`);
});
