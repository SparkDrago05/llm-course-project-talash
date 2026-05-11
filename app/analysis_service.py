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
from app.m3_analysis import (
    analyze_books,
    analyze_coauthor_patterns,
    analyze_patents,
    analyze_skill_alignment,
    analyze_supervision_profile,
    analyze_topic_variability,
    summarize_research_quality,
)
from app.profile_parser import parse_cv_structured
from app.summarizer import build_candidate_summary


def calculate_ranking_score(structured_data: dict, weights: dict = None) -> float:
    if weights is None:
        weights = {"education": 0.25, "experience": 0.2, "research": 0.3, "skills": 0.15, "m3": 0.1}
    
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

    # 5. Milestone 3 enrichment (topic diversity + coauthor network + supervision impact)
    topic_variability = analyze_topic_variability(structured_data.get("publications", []))
    coauthor_analysis = analyze_coauthor_patterns(
        structured_data.get("publications", []),
        structured_data.get("personal_info", {}).get("name", ""),
    )
    supervision_analysis = analyze_supervision_profile(
        structured_data.get("supervision", []),
        structured_data.get("publications", []),
    )
    m3_score = min(
        topic_variability.get("variability_score", 0) * 0.4
        + coauthor_analysis.get("collaboration_diversity_score", 0) * 0.4
        + min(supervision_analysis.get("papers_with_supervised_students", 0) * 10, 100) * 0.2,
        100,
    )

    m3_weight = weights.get("m3", 0.0)

    score = (min(edu_score, 100) * weights["education"]) + \
            (min(exp_score, 100) * weights["experience"]) + \
            (min(research_score, 100) * weights["research"]) + \
            (min(skills_score, 100) * weights["skills"]) + \
            (m3_score * m3_weight)

    return round(score, 2)


def process_candidate_pdf(pdf_path: Path, ranking_weights: dict = None) -> dict[str, Any]:
    raw_text, raw_text_path = extract_and_store_raw_text(pdf_path, RAW_TEXT_DIR)
    structured = parse_cv_structured(pdf_path, raw_text)

    education_analysis = analyze_education(structured["education"])
    experience_analysis = analyze_experience(structured["experience"], structured["education"])
    research_profile = analyze_publications(structured["publications"])
    missing_info = detect_missing_information(structured)

    topic_variability = analyze_topic_variability(structured["publications"])
    coauthor_analysis = analyze_coauthor_patterns(structured["publications"], structured["personal_info"].get("name", ""))
    supervision_analysis = analyze_supervision_profile(structured.get("supervision", []), structured["publications"])
    books_analysis = analyze_books(structured.get("books", []), structured["personal_info"].get("name", ""))
    patents_analysis = analyze_patents(structured.get("patents", []), structured["personal_info"].get("name", ""))
    skill_alignment = analyze_skill_alignment(
        structured.get("skills", []),
        structured.get("experience", []),
        structured.get("publications", []),
        topic_variability,
    )
    research_quality = summarize_research_quality(structured.get("publications", []))

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
        "topic_variability": topic_variability,
        "coauthor_analysis": coauthor_analysis,
        "supervision_analysis": supervision_analysis,
        "books_analysis": books_analysis,
        "patents_analysis": patents_analysis,
        "skill_alignment": skill_alignment,
        "research_quality": research_quality,
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
