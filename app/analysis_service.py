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
from app.profile_parser import parse_cv_structured
from app.summarizer import build_candidate_summary


def calculate_ranking_score(structured_data: dict, weights: dict = None) -> float:
    if weights is None:
        weights = {"education": 0.3, "experience": 0.2, "research": 0.4, "skills": 0.1}
    
    score = 0.0
    
    # 1. Education
    edu_score = 0
    if structured_data.get("education"):
        scores = []
        for e in structured_data["education"]:
            p = e.get("percentage")
            c = e.get("cgpa")
            if p is not None:
                scores.append(float(p))
            elif c is not None:
                scores.append(float(c) * 10)
            else:
                scores.append(0)
        edu_score = sum(scores) / len(scores) if scores else 0
    
    # 2. Experience
    exp_score = len(structured_data.get("experience", [])) * 10 
    
    # 3. Research
    pubs = structured_data.get("publications", [])
    research_score = len(pubs) * 5
    for pub in pubs:
        if pub.get("api_info", {}).get("inferred_quartile") == "Q1":
            research_score += 10

    # 4. Skills
    skills_score = min(len(structured_data.get("skills", [])), 20) * 2

    score = (min(edu_score, 100) * weights["education"]) + \
            (min(exp_score, 100) * weights["experience"]) + \
            (min(research_score, 100) * weights["research"]) + \
            (min(skills_score, 100) * weights["skills"])

    return round(score, 2)


def process_candidate_pdf(pdf_path: Path, ranking_weights: dict = None) -> dict[str, Any]:
    raw_text, raw_text_path = extract_and_store_raw_text(pdf_path, RAW_TEXT_DIR)
    structured = parse_cv_structured(pdf_path, raw_text)

    education_analysis = analyze_education(structured["education"])
    experience_analysis = analyze_experience(structured["experience"], structured["education"])
    research_profile = analyze_publications(structured["publications"])
    missing_info = detect_missing_information(structured)

    ranking_score = calculate_ranking_score(structured, ranking_weights)

    name = structured["personal_info"].get("name", pdf_path.stem)

    email_draft = build_missing_info_email(name, missing_info)
    summary = build_candidate_summary(name, education_analysis, experience_analysis, missing_info)

    return {
        "name": name,
        "personal_info": structured["personal_info"],
        "structured_data": structured,
        "education_analysis": education_analysis,
        "experience_analysis": experience_analysis,
        "research_profile": research_profile,
        "ranking_score": ranking_score,
        "missing_info": missing_info,
        "summary": summary,
        "email_draft": email_draft,
        "raw_text_path": str(raw_text_path),
    }


def process_candidates_from_pdfs(pdf_paths: list[Path], ranking_weights: dict = None) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    failed_files: list[str] = []

    for pdf_path in pdf_paths:
        try:
            candidates.append(process_candidate_pdf(pdf_path, ranking_weights))
        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")
            failed_files.append(pdf_path.name)
            
    # Sort candidates by ranking score
    candidates.sort(key=lambda x: x.get("ranking_score", 0), reverse=True)

    payload = {
        "processed_files": len(pdf_paths),
        "candidates": candidates,
        "failed_files": failed_files,
    }
    M2_RESULTS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload
