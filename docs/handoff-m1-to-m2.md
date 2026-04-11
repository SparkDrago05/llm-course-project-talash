# Handoff: Milestone 1 to Milestone 2

## Delivered in Milestone 1
1. FastAPI preprocessing service with upload, batch processing, and result endpoints.
2. CV text extraction and deterministic parser for core entities.
3. Linked CSV exports for candidates, education, experience, skills, publications, supervision, patents, and books.
4. Architecture, ingestion, schema, and UI/UX artifacts.

## Interface Contract for Milestone 2
1. Input source: PDF files in data/input or API upload endpoint.
2. Output tables in data/output with candidate_id as the join key.
3. Quality endpoint: GET /results/report for extraction completeness summary.

## Known Limitations
1. Parser is section-header driven and may miss unconventional CV formats.
2. External ranking verification (THE, QS, Scopus, WoS, CORE) is not integrated yet.
3. No persistent SQL database yet; CSV storage is used for Milestone 1 speed.

## Priority Next Tasks for Milestone 2 Owner
1. Implement education profile analysis logic and normalization scoring.
2. Implement professional experience timeline analysis.
3. Implement missing-information detection and personalized email drafting.
4. Start partial research profile verification with external data sources.
