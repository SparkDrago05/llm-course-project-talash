import re
from pathlib import Path
from typing import Any

from app.normalize import normalize_candidate_id, normalize_whitespace

YEAR_RE = re.compile(r"(19|20)\d{2}")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
CGPA_RE = re.compile(r"(\d(?:\.\d{1,2})?)\s*/\s*(\d(?:\.\d{1,2})?)")
PERCENT_RE = re.compile(r"(\d{2,3}(?:\.\d{1,2})?)\s*%")


SECTION_HINTS = {
    "education": ["education", "academic", "qualification"],
    "experience": ["experience", "employment", "work history", "professional"],
    "skills": ["skills", "technical skills", "competencies"],
    "publications": ["publications", "research", "papers"],
}


def _lines(text: str) -> list[str]:
    return [normalize_whitespace(line) for line in text.splitlines() if line.strip()]


def _extract_years(line: str) -> tuple[int | None, int | None]:
    years = [int(match.group(0)) for match in YEAR_RE.finditer(line)]
    if not years:
        return None, None
    if len(years) == 1:
        return years[0], None
    return min(years), max(years)


def _extract_score(line: str) -> dict[str, Any]:
    cgpa_match = CGPA_RE.search(line)
    pct_match = PERCENT_RE.search(line)
    cgpa = None
    cgpa_scale = None
    percentage = None
    score_raw = ""

    if cgpa_match:
        cgpa = float(cgpa_match.group(1))
        cgpa_scale = float(cgpa_match.group(2))
        score_raw = cgpa_match.group(0)
        if cgpa_scale > 0:
            percentage = round((cgpa / cgpa_scale) * 100, 2)

    if pct_match:
        percentage = float(pct_match.group(1))
        score_raw = pct_match.group(0)

    return {
        "score_raw": score_raw,
        "cgpa": cgpa,
        "cgpa_scale": cgpa_scale,
        "percentage": percentage,
    }


def _detect_section(line: str) -> str:
    value = line.lower()
    for section, hints in SECTION_HINTS.items():
        if any(hint in value for hint in hints):
            return section
    return ""


def _split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {
        "education": [],
        "experience": [],
        "skills": [],
        "publications": [],
    }
    active = ""
    for line in _lines(text):
        section = _detect_section(line)
        if section:
            active = section
            continue
        if active:
            sections[active].append(line)
    return sections


def _education_level(line: str) -> str:
    lowered = line.lower()
    if any(word in lowered for word in ["sse", "matric", "secondary school", "ssc"]):
        return "SSE"
    if any(word in lowered for word in ["hssc", "intermediate", "higher secondary", "hsc"]):
        return "HSSC"
    if any(word in lowered for word in ["phd", "mphil", "ms", "msc", "postgraduate"]):
        return "PG"
    if any(word in lowered for word in ["bs", "bsc", "be", "bachelor", "undergraduate"]):
        return "UG"
    return "OTHER"


def _extract_education(education_lines: list[str]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for line in education_lines:
        level = _education_level(line)
        if level == "OTHER":
            continue

        start_year, end_year = _extract_years(line)
        score = _extract_score(line)

        entries.append(
            {
                "level": level,
                "degree": line,
                "institution": "",
                "board": "" if level not in {"SSE", "HSSC"} else line,
                "start_year": start_year,
                "end_year": end_year,
                **score,
                "raw": line,
            }
        )

    return entries


def _extract_experience(experience_lines: list[str]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for line in experience_lines:
        start_year, end_year = _extract_years(line)
        if start_year is None and end_year is None:
            continue

        parts = [part.strip() for part in re.split(r"-|\||,", line) if part.strip()]
        job_title = parts[0] if parts else line
        organization = parts[1] if len(parts) > 1 else ""

        entries.append(
            {
                "job_title": job_title,
                "organization": organization,
                "start_date": str(start_year) if start_year else "",
                "end_date": str(end_year) if end_year else "Present",
                "start_year": start_year,
                "end_year": end_year,
                "raw": line,
            }
        )

    return entries


def _extract_skills(skill_lines: list[str], text: str) -> list[str]:
    candidates = []
    if skill_lines:
        candidates = skill_lines
    else:
        for line in _lines(text):
            if "skill" in line.lower():
                candidates.append(line)

    skills: list[str] = []
    for candidate in candidates:
        chunks = [item.strip(" .") for item in re.split(r",|;|\|", candidate) if item.strip()]
        for chunk in chunks:
            if len(chunk) > 1 and "skill" not in chunk.lower():
                skills.append(chunk)

    deduped: list[str] = []
    for skill in skills:
        if skill.lower() not in {item.lower() for item in deduped}:
            deduped.append(skill)
    return deduped


def _extract_publications(lines: list[str]) -> list[dict[str, Any]]:
    publications: list[dict[str, Any]] = []
    for line in lines:
        cleaned = line.strip("-• ")
        if len(cleaned) < 8:
            continue

        start_year, end_year = _extract_years(cleaned)
        year = end_year or start_year
        lowered = cleaned.lower()
        pub_type = "unknown"
        if "journal" in lowered:
            pub_type = "journal"
        elif any(word in lowered for word in ["conference", "proceedings", "ieee", "acm"]):
            pub_type = "conference"

        publications.append(
            {
                "title": cleaned,
                "year": year,
                "type": pub_type,
                "raw": line,
            }
        )
    return publications


def parse_cv_structured(pdf_path: Path, text: str) -> dict[str, Any]:
    lines = _lines(text)
    sections = _split_sections(text)
    candidate_id = normalize_candidate_id(pdf_path.stem)

    email_match = EMAIL_RE.search(text)

    personal_info = {
        "candidate_id": candidate_id,
        "name": lines[0] if lines else pdf_path.stem,
        "email": email_match.group(0) if email_match else "",
    }

    education = _extract_education(sections["education"])
    experience = _extract_experience(sections["experience"])
    skills = _extract_skills(sections["skills"], text)
    publications = _extract_publications(sections["publications"])

    return {
        "personal_info": personal_info,
        "education": education,
        "experience": experience,
        "skills": skills,
        "publications": publications,
    }
