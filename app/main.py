import json
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import INPUT_DIR, M2_RESULTS_JSON, OUTPUT_DIR, ensure_directories
from app.ingestion import list_pdf_files
from app.m2_service import process_candidates_from_pdfs
from app.processor import process_pdf_batch
from app.reporting import build_preprocessing_report
from app.schemas import IngestResponse, ProcessResponse, ReportResponse
from app.storage import write_outputs


app = FastAPI(title="TALASH Milestone 1 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    batch_result = process_pdf_batch(pdfs)
    if not batch_result.records:
        raise HTTPException(status_code=400, detail="All PDFs failed to parse")

    output_files = write_outputs(batch_result.records)

    return ProcessResponse(
        processed_files=len(pdfs),
        candidates=len(batch_result.records),
        output_files=output_files,
        failed_files=batch_result.failed_files,
    )


@app.get("/results/candidates")
def results_candidates() -> dict:
    csv_path = Path("data/output/candidates.csv")
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Candidates output not generated yet")

    rows = csv_path.read_text(encoding="utf-8").splitlines()
    return {"file": str(csv_path), "rows": rows[:20]}


@app.get("/results/report", response_model=ReportResponse)
def results_report() -> ReportResponse:
    csv_path = Path("data/output/candidates.csv")
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Candidates output not generated yet")

    report = build_preprocessing_report(OUTPUT_DIR)
    return ReportResponse(**report)


@app.post("/m2/ingest")
async def ingest_multiple_cvs(files: list[UploadFile] = File(...)) -> dict:
    saved_files: list[str] = []
    rejected_files: list[str] = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            rejected_files.append(file.filename)
            continue

        destination = INPUT_DIR / file.filename
        content = await file.read()
        destination.write_bytes(content)
        saved_files.append(str(destination))

    if not saved_files:
        raise HTTPException(status_code=400, detail="No valid PDF files uploaded")

    return {
        "saved": saved_files,
        "rejected": rejected_files,
        "message": "PDF CVs uploaded successfully",
    }


@app.post("/m2/process/all")
def process_m2_all() -> dict:
    pdfs = list_pdf_files(INPUT_DIR)
    if not pdfs:
        raise HTTPException(status_code=400, detail="No PDFs found in data/input")

    return process_candidates_from_pdfs(pdfs)


@app.post("/m2/upload-and-process")
async def m2_upload_and_process(files: list[UploadFile] = File(...)) -> dict:
    uploaded_pdfs: list[Path] = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"Only PDF supported: {file.filename}")
        destination = INPUT_DIR / file.filename
        content = await file.read()
        destination.write_bytes(content)
        uploaded_pdfs.append(destination)

    return process_candidates_from_pdfs(uploaded_pdfs)


@app.get("/m2/results/latest")
def m2_results_latest() -> dict:
    if not M2_RESULTS_JSON.exists():
        raise HTTPException(status_code=404, detail="Milestone 2 results not generated yet")

    return json.loads(M2_RESULTS_JSON.read_text(encoding="utf-8"))


@app.get("/m2/dashboard")
def m2_dashboard() -> dict:
    if not M2_RESULTS_JSON.exists():
        raise HTTPException(status_code=404, detail="Milestone 2 results not generated yet")

    payload = json.loads(M2_RESULTS_JSON.read_text(encoding="utf-8"))
    candidates = payload.get("candidates", [])

    table = []
    education_score_comparison = []
    experience_duration = []
    missing_info_count = []

    for candidate in candidates:
        name = candidate.get("name", "Unknown")
        education_score = candidate.get("education_analysis", {}).get("average_score", 0)
        experience_years = candidate.get("experience_analysis", {}).get("experience_duration_years", 0)
        missing_count = len(candidate.get("missing_info", []))

        table.append(
            {
                "name": name,
                "education_score": education_score,
                "experience_summary": \
candidate.get("experience_analysis", {}).get("career_progression", "undetermined"),
                "missing_info_flag": missing_count > 0,
            }
        )
        education_score_comparison.append({"name": name, "score": education_score})
        experience_duration.append({"name": name, "years": experience_years})
        missing_info_count.append({"name": name, "count": missing_count})

    return {
        "table": table,
        "charts": {
            "education_score_comparison": education_score_comparison,
            "experience_duration": experience_duration,
            "missing_info_count": missing_info_count,
        },
    }
