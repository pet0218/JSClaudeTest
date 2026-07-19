import { NavLink, Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./pages/Home";
import ReportProblem from "./pages/ReportProblem";

function App() {
  return (
    <div className="app">
      <h1>Finance Tracker</h1>
      <p className="subtitle">Track your income and expenses</p>

      <nav className="main-nav">
        <NavLink to="/" end>
          Prehľad
        </NavLink>
        <NavLink to="/report">Nahlásiť problém</NavLink>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/report" element={<ReportProblem />} />
      </Routes>
    </div>
  );
}

export default App;
