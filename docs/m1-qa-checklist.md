# Milestone 1 QA Checklist

Run this checklist before final demo/presentation.

## Setup
1. Dependencies install successfully from requirements.txt.
2. API launches with uvicorn app.main:app --reload.
3. data/input and data/output folders exist.

## Functional Checks
1. POST /ingest accepts PDF and saves it to data/input.
2. POST /ingest rejects non-PDF uploads.
3. POST /process/all processes valid files and returns failed_files for bad files.
4. GET /results/candidates returns preview rows after processing.
5. GET /results/report returns completeness metrics after processing.

## Output Checks
1. Linked CSVs are generated:
   - candidates.csv
   - education.csv
   - experience.csv
   - skills.csv
   - publications.csv
   - supervision.csv
   - patents.csv
   - books.csv
2. candidate_id is consistent across all output tables.

## Evidence Checks
1. docs/m1-traceability.md is up to date.
2. docs/demo.md runbook is current.
3. docs/wireframes contains all three screens.
4. docs/demo-assets contains screenshot checklist.
