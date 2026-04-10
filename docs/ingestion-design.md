# Folder-based CV Ingestion Design

## Pipeline
1. Accept file upload through `POST /ingest`.
2. Save uploaded PDFs in `data/input`.
3. Batch processor reads all PDFs from input folder via `POST /process/all`.
4. For each file:
   - extract text
   - parse sections
   - generate candidate entities
5. Export consolidated tables into `data/output`.

## Error Strategy
- Reject non-PDF uploads.
- Return a clear error when no PDFs are present.
- Keep parser tolerant to missing sections and continue processing.

## Milestone 2 Extension Points
- Add file watcher or queue worker.
- Add per-file processing status table.
- Add retries for extraction failures.
