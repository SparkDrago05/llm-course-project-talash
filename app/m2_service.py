import json
from pathlib import Path
from typing import Any

from app.analysis import (
    analyze_education,
    analyze_experience,
    analyze_publications,
    detect_missing_information,
)
from app.config import M2_RESULTS_JSON, RAW_TEXT_DIR
from app.emailer import build_missing_info_email
from app.ingestion import extract_and_store_raw_text
from app.m2_parser import parse_cv_structured
from app.summarizer import build_candidate_summary


def process_candidate_pdf(pdf_path: Path) -> dict[str, Any]:
    raw_text, raw_text_path = extract_and_store_raw_text(pdf_path, RAW_TEXT_DIR)
    structured = parse_cv_structured(pdf_path, raw_text)

    education_analysis = analyze_education(structured["education"])
    experience_analysis = analyze_experience(structured["experience"], structured["education"])
    research_profile = analyze_publications(structured["publications"])
    missing_info = detect_missing_information(structured)

    name = structured["personal_info"].get("name", pdf_path.stem)

    email_draft = build_missing_info_email(name, missing_info)
    summary = build_candidate_summary(name, education_analysis, experience_analysis, missing_info)

    return {
        "name": name,
        "personal_info": structured["personal_info"],
        "structured_data": {
            "education": structured["education"],
            "experience": structured["experience"],
            "skills": structured["skills"],
            "publications": structured["publications"],
        },
        "education_analysis": education_analysis,
        "experience_analysis": experience_analysis,
        "research_profile": research_profile,
        "missing_info": missing_info,
        "summary": summary,
        "email_draft": email_draft,
        "raw_text_path": str(raw_text_path),
    }


def process_candidates_from_pdfs(pdf_paths: list[Path]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    failed_files: list[str] = []

    for pdf_path in pdf_paths:
        try:
            candidates.append(process_candidate_pdf(pdf_path))
        except Exception:
            failed_files.append(pdf_path.name)

    payload = {
        "processed_files": len(pdf_paths),
        "candidates": candidates,
        "failed_files": failed_files,
    }
    M2_RESULTS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload
