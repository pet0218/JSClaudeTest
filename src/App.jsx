import { useState } from "react";
import "./App.css";
import { CATEGORIES } from "./constants/categories";
import { useTransactions } from "./hooks/useTransactions";
import { calculateTotals, filterTransactions } from "./utils/transactions";
import SummaryCards from "./components/SummaryCards";
import TransactionForm from "./components/TransactionForm";
import TransactionFilters from "./components/TransactionFilters";
import TransactionTable from "./components/TransactionTable";

function App() {
  const { transactions, addTransaction } = useTransactions();
  const [filterType, setFilterType] = useState("all");
  const [filterCategory, setFilterCategory] = useState("all");

  const { income, expenses, balance } = calculateTotals(transactions);
  const filteredTransactions = filterTransactions(transactions, {
    type: filterType,
    category: filterCategory,
  });

  return (
    <div className="app">
      <h1>Finance Tracker</h1>
      <p className="subtitle">Track your income and expenses</p>

      <SummaryCards income={income} expenses={expenses} balance={balance} />

      <TransactionForm categories={CATEGORIES} onAdd={addTransaction} />

      <div className="transactions">
        <h2>Transactions</h2>
        <TransactionFilters
          categories={CATEGORIES}
          filterType={filterType}
          filterCategory={filterCategory}
          onFilterTypeChange={setFilterType}
          onFilterCategoryChange={setFilterCategory}
        />
        <TransactionTable transactions={filteredTransactions} />
      </div>
    </div>
  );
}

export default App;
