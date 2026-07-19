import express from "express";
import cors from "cors";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { initialTransactions } from "./src/data/transactions.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPORTS_FILE = path.join(__dirname, "reports.json");

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

function readReports() {
  if (!fs.existsSync(REPORTS_FILE)) return [];
  return JSON.parse(fs.readFileSync(REPORTS_FILE, "utf-8"));
}

function writeReports(reports) {
  fs.writeFileSync(REPORTS_FILE, JSON.stringify(reports, null, 2));
}

app.get("/api/transactions", (req, res) => {
  res.json(initialTransactions);
});

app.get("/api/reports", (req, res) => {
  res.json(readReports());
});

app.post("/api/reports", (req, res) => {
  const { employeeName, employeeId, problem } = req.body;

  if (!employeeName || !employeeId || !problem) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  const report = {
    id: Date.now(),
    employeeName,
    employeeId,
    problem,
    createdAt: new Date().toISOString(),
  };

  const reports = readReports();
  reports.push(report);
  writeReports(reports);

  res.status(201).json(report);
});

app.listen(PORT, () => {
  console.log(`API server running at http://localhost:${PORT}`);
});
