import { useState } from "react";
import { initialTransactions } from "../data/transactions";

export function useTransactions() {
  const [transactions, setTransactions] = useState(initialTransactions);

  const addTransaction = ({ description, amount, type, category }) => {
    setTransactions((prev) => [
      ...prev,
      {
        id: Date.now(),
        description,
        amount: Number(amount),
        type,
        category,
        date: new Date().toISOString().split("T")[0],
      },
    ]);
  };

  return { transactions, addTransaction };
}
