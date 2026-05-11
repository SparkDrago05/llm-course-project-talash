# TALASH - Milestone 3 (Integrated)

This repository contains the integrated Milestone 3 implementation for TALASH (Smart HR Recruitment) for CS417 LLMs.

## Scope Covered (Milestone 3)
- Multi-CV PDF ingestion pipeline (folder + upload)
- Raw text extraction and storage per candidate
- Structured extraction for personal info, education, experience, skills, and publications
- Educational profile and professional timeline analysis
- Missing-information detection + personalized email draft generation
- Candidate summary generation
- Research profile enrichment (indexed signal, quartile heuristic, authorship role)
- Topic variability analysis (dominant topic, diversity score, trend)
- Co-author collaboration analysis (network size, recurring collaborations, diversity score)
- Supervision analysis (main/co-supervisor counts, student-linked publication signals)
- Books and patents extraction with role interpretation
- Skill alignment analysis (strong/partial/weak/unsupported evidence)
- Quantifiable weighted candidate ranking with configurable M3 contribution
- Web UI dashboard with comparative charts for M3 metrics

## Quick Start
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start API:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Open docs:
   - Swagger: http://127.0.0.1:8000/docs

## Backend API Endpoints
- `GET /health`

Milestone 1 compatibility:
- `POST /ingest` (multipart PDF)
- `POST /process/all` (process all PDFs from `data/input`)
- `GET /results/candidates`
- `GET /results/report`

Milestone 2 endpoints:
- `POST /m2/ingest` (upload multiple CV PDFs)
- `POST /m2/process/all` (auto-read all PDFs from `data/input`)
- `POST /m2/upload-and-process` (upload selected PDFs and process only uploaded files)
- `GET /m2/results/latest` (latest JSON result)
- `GET /m2/dashboard` (table rows + chart-ready aggregates)

`POST /m2/process/all` writes consolidated JSON output to `data/output/milestone2_candidates.json`.

## Tests
Run quick checks with:
```bash
pytest -q
```

Minimal syntax check:
```bash
python -m py_compile app/*.py tests/*.py
```

## Milestone 3 Output Format
Each candidate includes the required fields:

```json
{
   "name": "",
   "education_analysis": {"...": "..."},
   "experience_analysis": {"...": "..."},
   "research_quality": {"...": "..."},
   "topic_variability": {"...": "..."},
   "coauthor_analysis": {"...": "..."},
   "supervision_analysis": {"...": "..."},
   "books_analysis": {"...": "..."},
   "patents_analysis": {"...": "..."},
   "skill_alignment": {"...": "..."},
   "ranking_score": 0,
   "missing_info": [],
   "summary": "",
   "email_draft": ""
}
```

Additional supporting fields are included (`personal_info`, `structured_data`, `research_profile`, `raw_text_path`) for traceability.

## Frontend (Sample Intermediate UI)
The sample frontend is under `frontend/` and uses React + Vite.

Run it with:
```bash
cd frontend
npm install
npm run dev
```

Backend should be running on `http://127.0.0.1:8000`.

## Demo (Quick)
1. Put 1-2 PDF CVs in `data/input`.
2. Start server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. In browser open: http://127.0.0.1:8000/docs
4. Run endpoints in order:
   - `POST /process/all`
   - `GET /results/candidates`
   - `GET /results/report`
5. Show generated files under `data/output`.

## Milestone 1 Evidence (Reference)
- Requirement traceability: `docs/m1-traceability.md`
- Architecture and design docs: `docs/`
- UI/UX design notes: `docs/ui-ux.md`
- Wireframes: `docs/wireframes/`
- Demo runbook: `docs/demo.md`
- Demo evidence checklist: `docs/demo-assets/README.md`
- Optional demo script: `scripts/demo_run.sh`

## Notes
- `.local/worklog.md` is intentionally ignored from git.
- Extraction and analysis in M2 are deterministic/rule-based and intentionally modular for M3 LLM upgrades.
