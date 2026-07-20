import { useState } from "react";

const API_URL = "/api/reports";

function ReportProblem() {
  const [employeeName, setEmployeeName] = useState("");
  const [employeeId, setEmployeeId] = useState("");
  const [problem, setProblem] = useState("");
  const [status, setStatus] = useState("idle"); // idle | saving | success | error

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!employeeName || !employeeId || !problem) return;

    setStatus("saving");
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ employeeName, employeeId, problem }),
      });
      if (!res.ok) throw new Error("Request failed");

      setEmployeeName("");
      setEmployeeId("");
      setProblem("");
      setStatus("success");
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="report-problem">
      <h2>Nahlásiť problém</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Meno zamestnanca"
          value={employeeName}
          onChange={(e) => setEmployeeName(e.target.value)}
        />
        <input
          type="text"
          placeholder="ID zamestnanca"
          value={employeeId}
          onChange={(e) => setEmployeeId(e.target.value)}
        />
        <textarea
          placeholder="Popis problému"
          value={problem}
          onChange={(e) => setProblem(e.target.value)}
          rows={5}
        />
        <button type="submit" disabled={status === "saving"}>
          {status === "saving" ? "Odosielam…" : "Odoslať"}
        </button>
      </form>

      {status === "success" && (
        <p className="form-status form-status-success">Uložené.</p>
      )}
      {status === "error" && (
        <p className="form-status form-status-error">
          Uloženie zlyhalo. Skontroluj, či beží backend server (npm run server).
        </p>
      )}
    </div>
  );
}

export default ReportProblem;
