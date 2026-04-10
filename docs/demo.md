# Milestone 1 Demo Runbook

## Preconditions
1. Python environment is active.
2. Dependencies installed from requirements.txt.
3. At least one CV PDF is present in data/input.

## Demo Steps (5-7 minutes)
1. Start API:
   - uvicorn app.main:app --reload
2. Open Swagger docs at http://127.0.0.1:8000/docs
3. Execute POST /process/all
4. Execute GET /results/candidates
5. Execute GET /results/report
6. Show generated output files under data/output.

## Evidence to Show During Demo
1. Structured linked CSV tables for extracted entities.
2. Candidate preview output from API.
3. Completeness percentages from preprocessing report endpoint.
4. Design documents in docs/ for architecture, ingestion, schema, and LLM plan.

## Optional One-command Demo
- bash scripts/demo_run.sh
