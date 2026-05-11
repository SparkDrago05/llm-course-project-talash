import re
import requests
from pathlib import Path
from typing import Any

from app.normalize import normalize_candidate_id, normalize_whitespace

YEAR_RE = re.compile(r"(19|20)\d{2}")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
CGPA_RE = re.compile(r"(\d(?:\.\d{1,2})?)\s*/\s*(\d(?:\.\d{1,2})?)")
PERCENT_RE = re.compile(r"(\d{2,3}(?:\.\d{1,2})?)\s*%")
STANDALONE_CGPA_RE = re.compile(r"\b([23]\.\d{1,2}|4\.0)\b")
STANDALONE_PERCENT_RE = re.compile(r"\b([4-9]\d(?:\.\d{1,2})?|100)\b")
ISBN_RE = re.compile(r"(?:ISBN(?:-1[03])?:?\s*)?((?:97[89][\-\s]?)?[\d\-\s]{9,17}[\dxX])")
PATENT_NO_RE = re.compile(r"\b(?:[A-Z]{1,3}\d{4,}|\d{6,})\b")
URL_RE = re.compile(r"https?://\S+")


SECTION_HINTS = {
    "education": ["education", "academic", "qualification"],
    "experience": ["experience", "employment", "work history", "professional"],
    "skills": ["skills", "technical skills", "competencies"],
    "publications": ["publications", "research", "papers"],
    "supervision": ["supervision", "supervised", "students", "thesis"],
    "books": ["books", "authored", "monographs"],
    "patents": ["patents", "innovations", "intellectual property"],
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
    elif pct_match:
        percentage = float(pct_match.group(1))
        score_raw = pct_match.group(0)
    else:
        # Fallback to standalone numbers
        m_s_perc = STANDALONE_PERCENT_RE.search(line)
        if m_s_perc:
            percentage = float(m_s_perc.group(1))
            score_raw = m_s_perc.group(0)
        else:
            m_s_cgpa = STANDALONE_CGPA_RE.search(line)
            if m_s_cgpa:
                cgpa = float(m_s_cgpa.group(1))
                cgpa_scale = 4.0
                score_raw = m_s_cgpa.group(0)

    if cgpa is not None and cgpa_scale and cgpa_scale > 0:
        percentage = round((cgpa / cgpa_scale) * 100, 2)

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
        "supervision": [],
        "books": [],
        "patents": [],
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


def lookup_openalex_venue(query: str) -> dict:
    try:
        # Simplistic openalex check for venues to infer indexing / quality
        res = requests.get(f"https://api.openalex.org/venues?search={query}", timeout=2)
        if res.status_code == 200:
            data = res.json()
            if data.get("results"):
                top_result = data["results"][0]
                return {
                    "is_indexed": True,
                    "openalex_id": top_result.get("id"),
                    "display_name": top_result.get("display_name"),
                    "works_count": top_result.get("works_count", 0),
                    # Heuristic for Quartile based on citation count / works_count (just a dummy for project purposes)
                    "inferred_quartile": "Q1" if top_result.get("cited_by_count", 0) > 10000 else "Q2", 
                }
    except Exception:
        pass
    return {"is_indexed": False, "inferred_quartile": "Unknown"}


def _author_role(authors: list[str], candidate_name: str, text: str) -> str:
    candidate_lower = candidate_name.lower().strip()
    normalized = [author.lower().strip() for author in authors if author.strip()]
    corresponding_flag = "correspond" in text.lower() or "*" in text

    if not normalized:
        return "unknown"
    if normalized[0] == candidate_lower and corresponding_flag:
        return "first_and_corresponding"
    if normalized[0] == candidate_lower:
        return "first"
    if candidate_lower in normalized and corresponding_flag:
        return "corresponding"
    if candidate_lower in normalized:
        return "co-author"
    return "unknown"


def _extract_publications(lines: list[str], candidate_name: str) -> list[dict[str, Any]]:
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

        # Attempt to find the venue
        venue_query = ""
        if "journal of" in lowered:
            idx = lowered.find("journal of")
            venue_query = cleaned[idx:idx+30]
        elif "ieee" in lowered:
            venue_query = "ieee"

        api_info = {}
        if venue_query:
            api_info = lookup_openalex_venue(venue_query)

        # Basic co-author heuristics (assuming candidate name is known, but here we just list names roughly)
        authors_part = cleaned.split(".")[0] if "." in cleaned else ""
        authors = [a.strip() for a in authors_part.split(",") if len(a) > 3]

        candidate_role = _author_role(authors, candidate_name, cleaned)

        publications.append(
            {
                "title": cleaned,
                "year": year,
                "type": pub_type,
                "authors": authors,
                "candidate_authorship_role": candidate_role,
                "api_info": api_info,
                "raw": line,
            }
        )
    return publications


def _extract_supervision(lines: list[str]) -> list[dict[str, Any]]:
    supervision = []
    for line in lines:
        if len(line) < 5:
            continue
        lowered = line.lower()
        level = "MS" if "ms" in lowered or "master" in lowered or "mphil" in lowered else "PhD" if "phd" in lowered else "Unknown"
        role = "co-supervisor" if "co-supervisor" in lowered or "co supervisor" in lowered else "main-supervisor" if "supervisor" in lowered else "unspecified"
        year_match = YEAR_RE.search(line)
        student = re.split(r"[-,:;]", line)[0].strip()
        supervision.append(
            {
                "student": student,
                "level": level,
                "role": role,
                "graduation_year": int(year_match.group(0)) if year_match else None,
                "raw": line,
            }
        )
    return supervision


def _extract_books(lines: list[str]) -> list[dict[str, Any]]:
    books = []
    for line in lines:
        if len(line) < 5:
            continue
        isbn_match = ISBN_RE.search(line)
        year_match = YEAR_RE.search(line)
        url_match = URL_RE.search(line)

        parts = [part.strip() for part in re.split(r"\||;", line) if part.strip()]
        title = parts[0] if parts else line
        publisher = ""
        if len(parts) > 1:
            publisher = parts[1]
        elif "springer" in line.lower():
            publisher = "Springer"
        elif "ieee" in line.lower():
            publisher = "IEEE"

        authors = []
        if "," in title:
            authors = [item.strip() for item in title.split(",")[:-1] if item.strip()]

        books.append(
            {
                "title": title,
                "authors": authors,
                "isbn": isbn_match.group(1).strip() if isbn_match else "",
                "publisher": publisher,
                "publishing_year": int(year_match.group(0)) if year_match else None,
                "online_link": url_match.group(0) if url_match else "",
                "raw": line,
            }
        )
    return books


def _extract_patents(lines: list[str]) -> list[dict[str, Any]]:
    patents = []
    for line in lines:
        if len(line) < 5:
            continue
        number_match = PATENT_NO_RE.search(line)
        year_match = YEAR_RE.search(line)
        url_match = URL_RE.search(line)

        parts = [part.strip() for part in re.split(r"\||;", line) if part.strip()]
        title = parts[0] if parts else line
        inventors = [item.strip() for item in re.split(r",| and ", line) if len(item.strip()) > 3][:4]

        country = ""
        for token in ["pakistan", "usa", "uk", "china", "germany", "uae"]:
            if token in line.lower():
                country = token.upper()
                break

        patents.append(
            {
                "patent_number": number_match.group(0) if number_match else "",
                "title": title,
                "date": int(year_match.group(0)) if year_match else None,
                "inventors": inventors,
                "country": country,
                "online_link": url_match.group(0) if url_match else "",
                "raw": line,
            }
        )
    return patents


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
    publications = _extract_publications(sections["publications"], personal_info["name"])
    supervision = _extract_supervision(sections["supervision"])
    books = _extract_books(sections["books"])
    patents = _extract_patents(sections["patents"])

    return {
        "personal_info": personal_info,
        "education": education,
        "experience": experience,
        "skills": skills,
        "publications": publications,
        "supervision": supervision,
        "books": books,
        "patents": patents,
    }
