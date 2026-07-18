import express from "express";
import cors from "cors";
import { initialTransactions } from "./src/data/transactions.js";

const app = express();
const PORT = 3001;

app.use(cors());

app.get("/api/transactions", (req, res) => {
  res.json(initialTransactions);
});

app.listen(PORT, () => {
  console.log(`API server running at http://localhost:${PORT}`);
});
