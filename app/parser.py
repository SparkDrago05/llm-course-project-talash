import re
from pathlib import Path
from typing import Any
from rapidfuzz import fuzz

from app.extractor import extract_text_from_pdf


SECTION_HINTS = {
    "education": ["education", "academic background", "qualification"],
    "experience": ["experience", "employment", "work history"],
    "skills": ["skills", "technical skills", "competencies"],
    "publications": ["publications", "research", "papers"],
    "supervision": ["supervision", "students supervised", "supervised"],
    "patents": ["patents", "patent"],
    "books": ["books", "book chapters", "authored books"],
}


def _find_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _extract_email(text: str) -> str:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else ""


def _extract_phone(text: str) -> str:
    match = re.search(r"(\+?\d[\d\-\s]{8,}\d)", text)
    return match.group(0).strip() if match else ""


def _best_section(line: str) -> str:
    line_l = line.lower()
    best_name = ""
    best_score = 0
    for section, hints in SECTION_HINTS.items():
        for hint in hints:
            score = fuzz.ratio(line_l, hint)
            if score > best_score:
                best_score = score
                best_name = section
    return best_name if best_score >= 75 else ""


def parse_cv(pdf_path: Path) -> dict[str, Any]:
    text = extract_text_from_pdf(pdf_path)
    lines = _find_lines(text)

    name = lines[0] if lines else "Unknown Candidate"
    email = _extract_email(text)
    phone = _extract_phone(text)

    sections: dict[str, list[str]] = {
        "education": [],
        "experience": [],
        "skills": [],
        "publications": [],
        "supervision": [],
        "patents": [],
        "books": [],
    }

    active = ""
    for line in lines:
        detected = _best_section(line)
        if detected:
            active = detected
            continue
        if active:
            sections[active].append(line)

    return {
        "candidate": {
            "candidate_id": pdf_path.stem.lower().replace(" ", "_"),
            "name": name,
            "email": email,
            "phone": phone,
            "current_title": sections["experience"][0] if sections["experience"] else "",
        },
        "education": [{"candidate_id": pdf_path.stem, "entry": item} for item in sections["education"]],
        "experience": [{"candidate_id": pdf_path.stem, "entry": item} for item in sections["experience"]],
        "skills": [{"candidate_id": pdf_path.stem, "skill": item} for item in sections["skills"]],
        "publications": [
            {"candidate_id": pdf_path.stem, "entry": item} for item in sections["publications"]
        ],
        "supervision": [
            {"candidate_id": pdf_path.stem, "entry": item} for item in sections["supervision"]
        ],
        "patents": [{"candidate_id": pdf_path.stem, "entry": item} for item in sections["patents"]],
        "books": [{"candidate_id": pdf_path.stem, "entry": item} for item in sections["books"]],
    }
