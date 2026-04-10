from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile

from app.config import INPUT_DIR, ensure_directories
from app.parser import parse_cv
from app.schemas import IngestResponse, ProcessResponse
from app.storage import write_outputs


app = FastAPI(title="TALASH Milestone 1 API", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    ensure_directories()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
async def ingest_cv(file: UploadFile = File(...)) -> IngestResponse:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    destination = INPUT_DIR / file.filename
    content = await file.read()
    destination.write_bytes(content)
    return IngestResponse(file_name=file.filename, saved_to=str(destination))


@app.post("/process/all", response_model=ProcessResponse)
def process_all() -> ProcessResponse:
    pdfs = sorted(INPUT_DIR.glob("*.pdf"))
    if not pdfs:
        raise HTTPException(status_code=400, detail="No PDFs found in data/input")

    records = [parse_cv(pdf_path) for pdf_path in pdfs]
    output_files = write_outputs(records)

    return ProcessResponse(
        processed_files=len(pdfs),
        candidates=len(records),
        output_files=output_files,
    )


@app.get("/results/candidates")
def results_candidates() -> dict:
    csv_path = Path("data/output/candidates.csv")
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Candidates output not generated yet")

    rows = csv_path.read_text(encoding="utf-8").splitlines()
    return {"file": str(csv_path), "rows": rows[:20]}
