import { useMemo, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

function SimpleBarChart({ title, data, valueKey, color }) {
  const maxValue = Math.max(...data.map((item) => item[valueKey] || 0), 1);

  return (
    <div className="card">
      <h3>{title}</h3>
      <div className="chart">
        {data.map((item) => {
          const value = item[valueKey] || 0;
          const width = Math.max((value / maxValue) * 100, 2);
          return (
            <div key={`${title}-${item.name}`} className="bar-row">
              <div className="bar-label">{item.name}</div>
              <div className="bar-track">
                <div className="bar-fill" style={{ width: `${width}%`, background: color }} />
              </div>
              <div className="bar-value">{value}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function App() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [payload, setPayload] = useState(null);

  const candidates = useMemo(() => payload?.candidates || [], [payload]);

  async function handleUploadAndProcess() {
    setError("");
    if (!files.length) {
      setError("Please select one or more PDF CVs.");
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      files.forEach((file) => formData.append("files", file));

      const response = await fetch(`${API_BASE}/m2/upload-and-process`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const detail = await response.json();
        throw new Error(detail?.detail || "Upload failed");
      }

      const data = await response.json();
      setPayload(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  const chartEducation = candidates.map((candidate) => ({
    name: candidate.name,
    score: candidate.education_analysis?.average_score ?? 0,
  }));

  const chartExperience = candidates.map((candidate) => ({
    name: candidate.name,
    years: candidate.experience_analysis?.experience_duration_years ?? 0,
  }));

  const chartMissing = candidates.map((candidate) => ({
    name: candidate.name,
    count: (candidate.missing_info || []).length,
  }));

  return (
    <div className="container">
      <h1>TALASH - Milestone 2 Dashboard</h1>

      <div className="card">
        <h3>Upload CV PDFs</h3>
        <input
          type="file"
          accept="application/pdf"
          multiple
          onChange={(event) => setFiles(Array.from(event.target.files || []))}
        />
        <button onClick={handleUploadAndProcess} disabled={loading}>
          {loading ? "Processing..." : "Upload & Process"}
        </button>
        {error && <p className="error">{error}</p>}
      </div>

      <div className="card">
        <h3>Candidates</h3>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Education Score</th>
              <th>Experience Summary</th>
              <th>Missing Info Flag</th>
            </tr>
          </thead>
          <tbody>
            {candidates.map((candidate) => (
              <tr key={candidate.personal_info?.candidate_id || candidate.name}>
                <td>{candidate.name}</td>
                <td>{candidate.education_analysis?.average_score ?? 0}</td>
                <td>{candidate.experience_analysis?.career_progression ?? "undetermined"}</td>
                <td>{(candidate.missing_info || []).length ? "Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {!!candidates.length && (
        <div className="chart-grid">
          <SimpleBarChart
            title="Education Score Comparison"
            data={chartEducation}
            valueKey="score"
            color="#6366f1"
          />
          <SimpleBarChart
            title="Experience Duration"
            data={chartExperience}
            valueKey="years"
            color="#0ea5e9"
          />
          <SimpleBarChart
            title="Missing Info Count"
            data={chartMissing}
            valueKey="count"
            color="#f97316"
          />
        </div>
      )}
    </div>
  );
}
