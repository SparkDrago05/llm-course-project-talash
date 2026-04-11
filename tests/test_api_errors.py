from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_process_all_returns_400_when_no_pdfs() -> None:
    input_dir = Path("data/input")
    input_dir.mkdir(parents=True, exist_ok=True)

    # Keep only non-PDF files to force the expected error path.
    for path in input_dir.glob("*.pdf"):
        path.unlink()

    response = client.post("/process/all")
    assert response.status_code == 400
    assert response.json()["detail"] == "No PDFs found in data/input"


def test_results_report_returns_404_when_outputs_missing() -> None:
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    candidates_csv = output_dir / "candidates.csv"
    if candidates_csv.exists():
        candidates_csv.unlink()

    response = client.get("/results/report")
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidates output not generated yet"


def test_ingest_rejects_non_pdf_upload() -> None:
    response = client.post(
        "/ingest",
        files={"file": ("notes.txt", b"not a pdf", "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are supported"
