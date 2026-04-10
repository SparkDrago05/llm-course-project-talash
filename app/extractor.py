from pathlib import Path
import pdfplumber
import fitz


def extract_text_from_pdf(file_path: Path) -> str:
    # Primary extractor keeps layout better for rule-based parsing.
    text_chunks: list[str] = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)
    except Exception:
        text_chunks = []

    text = "\n".join(text_chunks).strip()
    if text:
        return text

    # Fallback extractor handles PDFs where pdfplumber returns empty pages.
    doc = fitz.open(file_path)
    try:
        return "\n".join(page.get_text("text") for page in doc).strip()
    finally:
        doc.close()
