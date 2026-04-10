# TALASH Milestone 1 Architecture

## High-level Flow
1. CV PDF files arrive in `data/input` (API upload or manual drop).
2. Preprocessing pipeline extracts text from PDF.
3. Rule-based parser splits candidate information into structured entities.
4. Storage writer exports linked CSV tables into `data/output`.
5. API exposes status and candidate preview for demo.

## Module Interaction
- Input Layer: FastAPI upload endpoint and folder reader
- Extraction Layer: `pdfplumber` with PyMuPDF fallback
- Parsing Layer: section detection and entity extraction
- Storage Layer: CSV outputs as linked tables
- Presentation Layer: API docs and response payloads for early prototype

## Milestone 1 Boundary
- Implemented: preprocessing and basic prototype endpoints
- Deferred: ranking, full analysis scoring, advanced dashboard, external ranking integrations
