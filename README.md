# TALASH - Milestone 1 Prototype

This repository contains the Milestone 1 implementation for TALASH (Smart HR Recruitment) for CS417 LLMs.

## Scope Covered (Milestone 1)
- Preprocessing module: PDF CV ingestion and structured extraction
- Architecture, ingestion, and schema design documentation
- Wireframe placeholders for UI flow
- Early API prototype for upload and processing

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

## Notes
- `.local/worklog.md` is intentionally ignored from git.
- Parser is deterministic in M1 and designed to be extended with LLM-based extraction in M2/M3.
