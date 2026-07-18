export function calculateTotals(transactions) {
  const income = transactions
    .filter((t) => t.type === "income")
    .reduce((sum, t) => sum + t.amount, 0);

  const expenses = transactions
    .filter((t) => t.type === "expense")
    .reduce((sum, t) => sum + t.amount, 0);

  return { income, expenses, balance: income - expenses };
}

export function filterTransactions(transactions, { type, category }) {
  return transactions.filter((t) => {
    if (type !== "all" && t.type !== type) return false;
    if (category !== "all" && t.category !== category) return false;
    return true;
  });
}
