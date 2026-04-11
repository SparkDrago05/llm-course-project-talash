# Milestone 1 Requirement Traceability

## Rubric Mapping

1. Architecture and technical design (4 marks)
- Evidence: docs/architecture.md
- Evidence: docs/ingestion-design.md
- Evidence: docs/llm-pipeline.md
- Evidence: docs/schema.md

2. UI/UX wireframes and design thinking (4 marks)
- Evidence: docs/wireframes/README.md
- Evidence: docs/wireframes/upload-view.svg
- Evidence: docs/wireframes/candidate-summary-dashboard.svg
- Evidence: docs/wireframes/candidate-detail-view.svg
- Evidence: docs/ui-ux.md

3. Preprocessing module plus early prototype (12 marks)
- Evidence: app/extractor.py (PDF extraction with fallback)
- Evidence: app/parser.py (section extraction and entity parsing)
- Evidence: app/storage.py (linked CSV export)
- Evidence: app/main.py endpoints:
  - GET /health
  - POST /ingest
  - POST /process/all
  - GET /results/candidates
  - GET /results/report

4. Running demo (5 marks)
- Evidence: API can ingest PDFs, process all CVs, and show extracted outputs and report.
- Action pending: demo script and screenshots in docs/demo.md and docs/demo-assets/

## Milestone 1 Scope Boundary
- Included: preprocessing pipeline, architecture docs, schema design, API prototype, report endpoint.
- Deferred to later milestones: complete research ranking integrations, topic modeling, full dashboard analytics, candidate ranking engine.
