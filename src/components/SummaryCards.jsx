function SummaryCards({ income, expenses, balance }) {
  return (
    <div className="summary">
      <div className="summary-card">
        <h3>Income</h3>
        <p className="income-amount">${income}</p>
      </div>
      <div className="summary-card">
        <h3>Expenses</h3>
        <p className="expense-amount">${expenses}</p>
      </div>
      <div className="summary-card">
        <h3>Balance</h3>
        <p className="balance-amount">${balance}</p>
      </div>
    </div>
  );
}

export default SummaryCards;
