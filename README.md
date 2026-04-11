# TALASH - Milestone 1 Prototype

This repository contains the Milestone 1 implementation for TALASH (Smart HR Recruitment) for CS417 LLMs.

## Scope Covered (Milestone 1)
- Preprocessing module: PDF CV ingestion and structured extraction
- Architecture, ingestion, and schema design documentation
- Wireframe placeholders for UI flow
- Early API prototype for upload and processing
- Extracted entities: education, experience, skills, publications, supervision, patents, books

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

## API Endpoints
- `GET /health`
- `POST /ingest` (multipart PDF)
- `POST /process/all` (process all PDFs from `data/input`)
- `GET /results/candidates`
- `GET /results/report`

`POST /process/all` writes linked CSV outputs in `data/output` for all extracted entities.
If some PDFs fail to parse, the endpoint still processes valid files and returns `failed_files`.

## Tests
Run quick checks with:
```bash
pytest -q
```

## Milestone 1 Evidence
- Requirement traceability: `docs/m1-traceability.md`
- Architecture and design docs: `docs/`
- UI/UX design notes: `docs/ui-ux.md`
- Wireframes: `docs/wireframes/`
- Demo runbook: `docs/demo.md`
- Demo evidence checklist: `docs/demo-assets/README.md`
- Handoff document: `docs/handoff-m1-to-m2.md`
- QA checklist: `docs/m1-qa-checklist.md`
- Optional demo script: `scripts/demo_run.sh`

## Notes
- `.local/worklog.md` is intentionally ignored from git.
- Parser is deterministic in M1 and designed to be extended with LLM-based extraction in M2/M3.
