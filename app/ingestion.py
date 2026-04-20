from pathlib import Path

from app.extractor import extract_text_from_pdf
from app.normalize import normalize_candidate_id


def list_pdf_files(input_dir: Path) -> list[Path]:
    return sorted(path for path in input_dir.glob("*.pdf") if path.is_file())


def extract_and_store_raw_text(pdf_path: Path, raw_text_dir: Path) -> tuple[str, Path]:
    text = extract_text_from_pdf(pdf_path)
    candidate_id = normalize_candidate_id(pdf_path.stem)
    destination = raw_text_dir / f"{candidate_id}.txt"
    destination.write_text(text, encoding="utf-8")
    return text, destination
