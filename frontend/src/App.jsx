import { useMemo, useState, useRef } from "react";

const API_BASE = "http://127.0.0.1:8000";

function Modal({ title, onClose, children }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>
  );
}

function SimpleBarChart({ title, data, valueKey, color, icon }) {
  const maxValue = Math.max(...data.map((item) => item[valueKey] || 0), 1);

  return (
    <div className="card">
      <h3><span>{icon}</span> {title}</h3>
      <div className="chart">
        {data.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>No data available</p>
        ) : (
          data.map((item) => {
            const value = item[valueKey] || 0;
            const width = Math.max((value / maxValue) * 100, 2);
            return (
              <div key={`${title}-${item.name}`} className="bar-row">
                <div className="bar-header">
                  <span className="bar-label" title={item.name}>{item.name.length > 30 ? item.name.substring(0,30)+'...' : item.name}</span>
                  <span className="bar-value">{value}</span>
                </div>
                <div className="bar-track">
                  <div className="bar-fill" style={{ width: `${width}%`, background: color }} />
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default function App() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [payload, setPayload] = useState(null);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [viewingEmail, setViewingEmail] = useState(null);
  const fileInputRef = useRef(null);
  
  const [weights, setWeights] = useState({
    education: 0.3,
    experience: 0.2,
    research: 0.4,
    skills: 0.1,
  });

  const candidates = useMemo(() => payload?.candidates || [], [payload]);

  async function handleUploadAndProcess() {
    setError("");
    if (!files.length) {
      setError("Please select one or more PDF CVs first.");
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      files.forEach((file) => formData.append("files", file));

      const response = await fetch(`${API_BASE}/api/upload-and-process`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const detail = await response.json();
        throw new Error(detail?.detail || "Parsing failed.");
      }

      const data = await response.json();
      setPayload(data);
      setFiles([]);
      if (fileInputRef.current) fileInputRef.current.value = "";
      await applyWeights(data.candidates);
    } catch (err) {
      setError(err.message || "An error occurred during processing.");
    } finally {
      setLoading(false);
    }
  }

  async function applyWeights(currentCandidates = candidates) {
    if (!currentCandidates.length) return;
    try {
      const response = await fetch(`${API_BASE}/api/rank`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(weights),
      });
      if (response.ok) {
        const data = await response.json();
        setPayload(prev => ({ ...prev, candidates: data.candidates }));
      }
    } catch (err) {
      console.error("Failed to apply ranking", err);
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

  const chartResearch = candidates.map((candidate) => ({
    name: candidate.name,
    count: candidate.structured_data?.publications?.length ?? 0,
  }));

  return (
    <div className="container">
      <header style={{ marginBottom: '40px' }}>
        <h1>TALASH <span style={{ color: 'var(--text-muted)', fontSize: '1rem', fontWeight: '400', marginLeft: '10px' }}>v3.1 Smart Recruitment</span></h1>
        <p style={{ color: 'var(--text-muted)', marginTop: '-20px' }}>Candidate Analysis & Profile Management System</p>
      </header>

      <div className="grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div className="card">
          <h3><span>📁</span> CV Ingestion</h3>
          <input
            ref={fileInputRef}
            type="file"
            accept="application/pdf"
            multiple
            onChange={(event) => {
              setError("");
              setFiles(Array.from(event.target.files || []));
            }}
          />
          <div style={{ marginTop: '16px', display: 'flex', alignItems: 'center', gap: '12px' }}>
            <button onClick={handleUploadAndProcess} disabled={loading || !files.length}>
              {loading ? "⚡ Processing..." : "🚀 Upload & Analyze"}
            </button>
          </div>
          {error && <div className="error-message"><span>⚠️</span> {error}</div>}
          {payload?.failed_files?.length > 0 && (
            <div className="error-message" style={{ background: 'rgba(245, 158, 11, 0.1)', color: '#fbbf24' }}>
              <span>⚠️</span> Failed: {payload.failed_files.join(", ")}
            </div>
          )}
        </div>

        <div className="card">
          <h3><span>⚖️</span> Ranking Weights</h3>
          <div className="ranking-inputs">
            {Object.keys(weights).map(key => (
              <div className="input-group" key={key}>
                <label style={{ textTransform: 'capitalize' }}>{key}</label>
                <input type="number" step="0.1" value={weights[key]} onChange={e => setWeights({...weights, [key]: parseFloat(e.target.value)})} />
              </div>
            ))}
          </div>
          <button className="secondary-btn" onClick={() => applyWeights()} disabled={!candidates.length || loading}>
            🔄 Recalculate Rankings
          </button>
        </div>
      </div>

      <div className="card" style={{ overflowX: 'auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3><span>🏆</span> Candidate Leaderboard</h3>
          {candidates.length > 0 && <span className="badge badge-success">{candidates.length} Profiles Analyzed</span>}
        </div>
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Score</th>
              <th>Candidate</th>
              <th>Education</th>
              <th>Experience</th>
              <th>Research</th>
              <th>Alerts</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {candidates.length === 0 ? (
              <tr><td colSpan="8" style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>No candidates analyzed yet.</td></tr>
            ) : (
              candidates.map((candidate, index) => (
                <tr key={candidate.personal_info?.candidate_id || candidate.name}>
                  <td style={{ fontWeight: '800', color: index === 0 ? 'var(--accent)' : 'inherit' }}>#{index + 1}</td>
                  <td><span className="score-badge">{candidate.ranking_score ?? 0}</span></td>
                  <td style={{ cursor: 'pointer' }} onClick={() => setSelectedCandidate(candidate)}>
                    <div style={{ fontWeight: '600' }} title={candidate.name}>{candidate.name.length > 40 ? candidate.name.substring(0,40)+'...' : candidate.name}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{candidate.personal_info?.email}</div>
                  </td>
                  <td>{candidate.education_analysis?.average_score ?? 0}%</td>
                  <td><span className="badge badge-warning">{candidate.experience_analysis?.career_progression ?? "N/A"}</span></td>
                  <td>{candidate.structured_data?.publications?.length ?? 0} Pubs</td>
                  <td>
                    {(candidate.missing_info || []).length > 0 ? (
                      <div className="tooltip-container">
                        <span className="badge badge-error">Missing Info ({candidate.missing_info.length})</span>
                        <div className="tooltip">
                          {candidate.missing_info.map(m => <div key={m}>• {m}</div>)}
                        </div>
                      </div>
                    ) : (
                      <span className="badge badge-success">Complete</span>
                    )}
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button className="icon-btn" onClick={() => setSelectedCandidate(candidate)} title="View Details">👁️</button>
                      {(candidate.missing_info || []).length > 0 && (
                        <button className="icon-btn" onClick={() => setViewingEmail(candidate)} title="Draft Email">✉️</button>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {candidates.length > 0 && (
        <div className="chart-grid">
          <SimpleBarChart title="Academic Performance" icon="🎓" data={chartEducation} valueKey="score" color="var(--primary)" />
          <SimpleBarChart title="Professional Tenure (Years)" icon="💼" data={chartExperience} valueKey="years" color="var(--accent)" />
          <SimpleBarChart title="Research Productivity" icon="🔬" data={chartResearch} valueKey="count" color="var(--secondary)" />
        </div>
      )}

      {/* Modals */}
      {selectedCandidate && (
        <Modal title="Candidate Profile Details" onClose={() => setSelectedCandidate(null)}>
          <div className="candidate-details">
            <div className="detail-section">
              <h4>Personal Information</h4>
              <p><strong>Name:</strong> {selectedCandidate.name}</p>
              <p><strong>Email:</strong> {selectedCandidate.personal_info?.email || "N/A"}</p>
              <p><strong>Candidate ID:</strong> {selectedCandidate.personal_info?.candidate_id}</p>
            </div>
            
            <div className="detail-grid">
              <div className="detail-section">
                <h4>Education Analysis</h4>
                <p><strong>Classification:</strong> {selectedCandidate.education_analysis?.strength_classification}</p>
                <p><strong>Average Score:</strong> {selectedCandidate.education_analysis?.average_score}%</p>
                <p><strong>Progression:</strong> {selectedCandidate.education_analysis?.progression_summary}</p>
                <h5>Entries:</h5>
                <ul>
                  {selectedCandidate.structured_data?.education?.map((e, i) => (
                    <li key={i}>{e.degree} - <span style={{color:'var(--accent)'}}>{e.percentage ? e.percentage+'%' : e.cgpa ? e.cgpa+'/'+e.cgpa_scale : 'N/A'}</span></li>
                  ))}
                </ul>
              </div>
              <div className="detail-section">
                <h4>Experience Analysis</h4>
                <p><strong>Duration:</strong> {selectedCandidate.experience_analysis?.experience_duration_years} years</p>
                <p><strong>Career Trend:</strong> {selectedCandidate.experience_analysis?.career_progression}</p>
                <h5>History:</h5>
                <ul>
                  {selectedCandidate.structured_data?.experience?.map((e, i) => (
                    <li key={i}>{e.job_title} @ {e.organization} ({e.start_year}-{e.end_year || 'Present'})</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="detail-section">
              <h4>Research & Publications</h4>
              <p>Total Publications: {selectedCandidate.structured_data?.publications?.length}</p>
              <div className="pub-list">
                {selectedCandidate.structured_data?.publications?.slice(0, 10).map((p, i) => (
                  <div key={i} className="pub-item">
                    <span>{p.type === 'journal' ? '📓' : '📄'}</span>
                    <div>
                      <strong>{p.title}</strong>
                      {p.api_info?.inferred_quartile && <span className={`q-badge ${p.api_info.inferred_quartile.toLowerCase()}`}>{p.api_info.inferred_quartile}</span>}
                    </div>
                  </div>
                ))}
                {selectedCandidate.structured_data?.publications?.length > 10 && <p>...and {selectedCandidate.structured_data.publications.length - 10} more.</p>}
              </div>
            </div>
          </div>
        </Modal>
      )}

      {viewingEmail && (
        <Modal title={`Draft Email: ${viewingEmail.name}`} onClose={() => setViewingEmail(null)}>
          <div className="email-draft-container">
            <textarea readOnly value={viewingEmail.email_draft} />
            <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'flex-end' }}>
              <button onClick={() => {
                navigator.clipboard.writeText(viewingEmail.email_draft);
                alert("Email draft copied to clipboard!");
              }}>📋 Copy to Clipboard</button>
            </div>
          </div>
        </Modal>
      )}
      
      <footer style={{ marginTop: '60px', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
        &copy; 2026 TALASH AI Recruitment System | Built for CS 417: Large Language Models
      </footer>
    </div>
  );
}
