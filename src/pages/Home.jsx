import { useState } from "react";
import { CATEGORIES } from "../constants/categories";
import { useTransactions } from "../hooks/useTransactions";
import { calculateTotals, filterTransactions } from "../utils/transactions";
import SummaryCards from "../components/SummaryCards";
import TransactionForm from "../components/TransactionForm";
import TransactionFilters from "../components/TransactionFilters";
import TransactionTable from "../components/TransactionTable";

function Home() {
  const { transactions, addTransaction } = useTransactions();
  const [filterType, setFilterType] = useState("all");
  const [filterCategory, setFilterCategory] = useState("all");

  const { income, expenses, balance } = calculateTotals(transactions);
  const filteredTransactions = filterTransactions(transactions, {
    type: filterType,
    category: filterCategory,
  });

  return (
    <>
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
    </>
  );
}

export default Home;
