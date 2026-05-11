from typing import Any


EDUCATION_ORDER = {"SSE": 1, "HSSC": 2, "UG": 3, "PG": 4}
ROLE_RANK = {
    "intern": 1,
    "junior": 2,
    "assistant": 3,
    "engineer": 4,
    "lecturer": 4,
    "senior": 5,
    "lead": 6,
    "manager": 7,
    "director": 8,
    "head": 9,
    "professor": 9,
}


def _safe_percentage(entry: dict[str, Any]) -> float | None:
    if entry.get("percentage") is not None:
        return float(entry["percentage"])
    cgpa = entry.get("cgpa")
    scale = entry.get("cgpa_scale")
    if cgpa is not None and scale:
        return round((float(cgpa) / float(scale)) * 100, 2)
    return None


def analyze_education(education: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_entries = sorted(
        education,
        key=lambda item: EDUCATION_ORDER.get(item.get("level", "OTHER"), 99),
    )

    progression = [entry.get("level", "OTHER") for entry in sorted_entries]
    progression_summary = " → ".join(progression) if progression else "No educational data found"

    percentages = [value for value in (_safe_percentage(item) for item in sorted_entries) if value is not None]
    score = round(sum(percentages) / len(percentages), 2) if percentages else 0.0

    grade_trend = "insufficient-data"
    if len(percentages) >= 2:
        grade_trend = "improving" if percentages[-1] >= percentages[0] else "declining"

    gaps: list[dict[str, Any]] = []
    for first, second in zip(sorted_entries, sorted_entries[1:]):
        end_year = first.get("end_year") or first.get("start_year")
        next_start = second.get("start_year") or second.get("end_year")
        if end_year and next_start and next_start - end_year > 1:
            gaps.append(
                {
                    "between": f"{first.get('level')}->{second.get('level')}",
                    "years": next_start - end_year,
                }
            )

    if score >= 75 and len(gaps) <= 1:
        strength = "Strong"
    elif score >= 55:
        strength = "متوسط"
    else:
        strength = "Weak"

    return {
        "progression": progression,
        "progression_summary": progression_summary,
        "grade_trend": grade_trend,
        "average_score": score,
        "gap_duration": gaps,
        "strength_classification": strength,
    }


def _role_score(job_title: str) -> int:
    title = (job_title or "").lower()
    max_rank = 0
    for keyword, rank in ROLE_RANK.items():
        if keyword in title:
            max_rank = max(max_rank, rank)
    return max_rank


def _duration(entry: dict[str, Any]) -> int:
    start_year = entry.get("start_year")
    end_year = entry.get("end_year") or start_year
    if start_year and end_year and end_year >= start_year:
        return end_year - start_year
    return 0


def analyze_experience(
    experience: list[dict[str, Any]],
    education: list[dict[str, Any]],
) -> dict[str, Any]:
    entries = sorted(
        [item for item in experience if item.get("start_year")],
        key=lambda item: item.get("start_year", 9999),
    )

    flags: list[str] = []
    timeline_lines: list[str] = []
    overlaps_between_jobs: list[dict[str, Any]] = []

    for item in entries:
        timeline_lines.append(
            f"{item.get('job_title', 'Role')} ({item.get('start_year', '?')} - {item.get('end_year', 'Present')})"
        )

    for first, second in zip(entries, entries[1:]):
        first_end = first.get("end_year") or first.get("start_year")
        second_start = second.get("start_year")
        if first_end and second_start:
            if second_start <= first_end:
                overlaps_between_jobs.append(
                    {
                        "first": first.get("raw", ""),
                        "second": second.get("raw", ""),
                    }
                )

    if overlaps_between_jobs:
        flags.append("Job timeline overlap detected")

    overlaps_with_education: list[dict[str, Any]] = []
    for job in entries:
        job_start = job.get("start_year")
        job_end = job.get("end_year") or job_start
        if not job_start or not job_end:
            continue

        for edu in education:
            edu_start = edu.get("start_year")
            edu_end = edu.get("end_year") or edu_start
            if not edu_start or not edu_end:
                continue

            if max(job_start, edu_start) <= min(job_end, edu_end):
                overlaps_with_education.append(
                    {
                        "job": job.get("raw", ""),
                        "education": edu.get("raw", ""),
                    }
                )

    if overlaps_with_education:
        flags.append("Experience overlaps with education period")

    employment_gaps: list[dict[str, Any]] = []
    for first, second in zip(entries, entries[1:]):
        first_end = first.get("end_year") or first.get("start_year")
        second_start = second.get("start_year")
        if first_end and second_start and second_start - first_end > 1:
            employment_gaps.append(
                {
                    "between": f"{first.get('job_title', 'Role')} -> {second.get('job_title', 'Role')}",
                    "years": second_start - first_end,
                }
            )

    if employment_gaps:
        flags.append("Employment gaps detected")

    role_scores = [_role_score(item.get("job_title", "")) for item in entries]
    progression = "undetermined"
    if len(role_scores) >= 2:
        progression = "progressing" if role_scores[-1] >= role_scores[0] else "stagnant-or-declining"

    total_years = sum(_duration(item) for item in entries)

    return {
        "timeline_report": timeline_lines,
        "overlap_between_jobs": overlaps_between_jobs,
        "overlap_with_education": overlaps_with_education,
        "employment_gaps": employment_gaps,
        "career_progression": progression,
        "experience_duration_years": total_years,
        "flags": flags,
    }


def analyze_publications(publications: list[dict[str, Any]]) -> dict[str, Any]:
    journal_count = sum(1 for item in publications if item.get("type") == "journal")
    conference_count = sum(1 for item in publications if item.get("type") == "conference")
    unknown_count = max(len(publications) - journal_count - conference_count, 0)

    return {
        "publication_count": len(publications),
        "publication_titles": [item.get("title", "") for item in publications if item.get("title")],
        "classification": {
            "journal": journal_count,
            "conference": conference_count,
            "unknown": unknown_count,
        },
    }


def detect_missing_information(candidate: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    education = candidate.get("education", [])
    experience = candidate.get("experience", [])
    publications = candidate.get("publications", [])
    supervision = candidate.get("supervision", [])
    books = candidate.get("books", [])
    patents = candidate.get("patents", [])

    for level in ["SSE", "HSSC", "UG", "PG"]:
        level_items = [item for item in education if item.get("level") == level]
        if level_items and not any(item.get("score_raw") for item in level_items):
            missing.append(f"{level} marks/CGPA")
        if level_items and not any(item.get("start_year") or item.get("end_year") for item in level_items):
            missing.append(f"{level} dates")

    for entry in experience:
        if not entry.get("start_year") or not entry.get("end_year"):
            missing.append("Experience duration (start/end date)")
            break

    if not publications:
        missing.append("Publication details")
    elif any(not item.get("title") for item in publications):
        missing.append("Publication title")
    else:
        if any(not item.get("year") for item in publications):
            missing.append("Publication year")
        if any(not item.get("authors") for item in publications):
            missing.append("Publication authorship")
        if any(item.get("type") == "unknown" for item in publications):
            missing.append("Publication venue/type clarity")

    if supervision and any(not item.get("level") or not item.get("student") for item in supervision):
        missing.append("Supervision details (student/level)")

    if books:
        if any(not item.get("title") for item in books):
            missing.append("Book title")
        if any(not item.get("publisher") for item in books):
            missing.append("Book publisher")
        if any(not item.get("isbn") for item in books):
            missing.append("Book ISBN")

    if patents:
        if any(not item.get("patent_number") for item in patents):
            missing.append("Patent number")
        if any(not item.get("inventors") for item in patents):
            missing.append("Patent inventors")
        if any(not item.get("country") for item in patents):
            missing.append("Patent country")

    unique_missing: list[str] = []
    for field in missing:
        if field not in unique_missing:
            unique_missing.append(field)

    return unique_missing
