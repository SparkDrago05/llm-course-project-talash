import math
import re
from collections import Counter, defaultdict
from statistics import mean
from typing import Any


THEME_KEYWORDS = {
    "machine_learning": [
        "machine learning",
        "deep learning",
        "neural",
        "transformer",
        "classification",
        "regression",
    ],
    "nlp": [
        "nlp",
        "natural language",
        "text mining",
        "language model",
        "sentiment",
        "token",
    ],
    "computer_vision": ["computer vision", "image", "object detection", "segmentation", "video"],
    "cybersecurity": ["cyber", "security", "malware", "intrusion", "forensics", "privacy"],
    "data_science": ["data mining", "analytics", "big data", "data science", "forecasting"],
    "software_engineering": ["software", "testing", "requirements", "architecture", "agile", "devops"],
    "networks_iot": ["network", "wireless", "iot", "sensor", "routing", "5g"],
    "hr_analytics": ["recruitment", "talent", "hiring", "human resources", "hr analytics"],
}

ROLE_KEYWORDS = {
    "main_supervisor": ["main supervisor", "principal supervisor", "primary supervisor", "supervisor"],
    "co_supervisor": ["co-supervisor", "co supervisor", "joint supervisor"],
}

PUBLISHER_HINTS = {
    "strong": ["springer", "wiley", "ieee", "acm", "elsevier", "oxford", "cambridge"],
    "moderate": ["crc", "taylor", "sage", "routledge", "pearson", "mcgraw"],
}


def _safe_name(value: str) -> str:
    text = (value or "").strip().lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def _match_theme(text: str) -> str:
    lowered = (text or "").lower()
    best_theme = "other"
    best_count = 0

    for theme, keywords in THEME_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword in lowered)
        if count > best_count:
            best_count = count
            best_theme = theme

    return best_theme


def analyze_topic_variability(publications: list[dict[str, Any]]) -> dict[str, Any]:
    if not publications:
        return {
            "dominant_topic": "none",
            "theme_distribution": {},
            "variability_score": 0.0,
            "specialization": "insufficient-data",
            "topic_trend_over_time": [],
        }

    theme_counts: Counter[str] = Counter()
    year_theme_counter: dict[int, Counter[str]] = defaultdict(Counter)

    for publication in publications:
        title = publication.get("title", "")
        theme = _match_theme(title)
        theme_counts[theme] += 1
        publication["inferred_theme"] = theme

        year = publication.get("year")
        if isinstance(year, int):
            year_theme_counter[year][theme] += 1

    total = sum(theme_counts.values())
    distribution = {theme: round((count / total) * 100, 2) for theme, count in theme_counts.items()}

    probabilities = [count / total for count in theme_counts.values() if count > 0]
    entropy = -sum(prob * math.log(prob, 2) for prob in probabilities)
    max_entropy = math.log(len(theme_counts), 2) if len(theme_counts) > 1 else 1.0
    normalized_entropy = entropy / max_entropy if max_entropy else 0.0
    variability_score = round(min(max(normalized_entropy * 100, 0), 100), 2)

    dominant_topic = theme_counts.most_common(1)[0][0]
    if variability_score <= 33:
        specialization = "highly-focused"
    elif variability_score <= 66:
        specialization = "moderately-diverse"
    else:
        specialization = "highly-diverse"

    trend = []
    for year in sorted(year_theme_counter.keys()):
        year_counts = year_theme_counter[year]
        top_theme = year_counts.most_common(1)[0][0]
        trend.append({"year": year, "dominant_theme": top_theme, "publications": sum(year_counts.values())})

    return {
        "dominant_topic": dominant_topic,
        "theme_distribution": distribution,
        "variability_score": variability_score,
        "specialization": specialization,
        "topic_trend_over_time": trend,
    }


def analyze_coauthor_patterns(publications: list[dict[str, Any]], candidate_name: str) -> dict[str, Any]:
    candidate_norm = _safe_name(candidate_name)
    collaborators: Counter[str] = Counter()
    coauthor_sizes: list[int] = []
    recurring_papers = 0

    for publication in publications:
        raw_authors = publication.get("authors", []) or []
        normalized = []
        for author in raw_authors:
            cleaned = _safe_name(author)
            if cleaned and cleaned != candidate_norm:
                normalized.append(cleaned)

        unique_coauthors = sorted(set(normalized))
        for collaborator in unique_coauthors:
            collaborators[collaborator] += 1

        if unique_coauthors:
            coauthor_sizes.append(len(unique_coauthors))
            if any(collaborators[name] > 1 for name in unique_coauthors):
                recurring_papers += 1

    publication_count = len(publications)
    recurring_ratio = round((recurring_papers / publication_count) * 100, 2) if publication_count else 0.0
    average_team_size = round(mean(coauthor_sizes), 2) if coauthor_sizes else 0.0

    frequent = [
        {"coauthor": name, "collaborations": count}
        for name, count in collaborators.most_common(5)
    ]

    if average_team_size >= 4:
        team_structure = "large-teams"
    elif average_team_size >= 2:
        team_structure = "medium-teams"
    elif average_team_size > 0:
        team_structure = "small-teams"
    else:
        team_structure = "solo-or-unknown"

    diversity_base = len(collaborators)
    density_penalty = max(recurring_ratio / 100, 0.01)
    diversity_score = round(min((diversity_base / (publication_count * density_penalty + 1)) * 20, 100), 2)

    return {
        "unique_coauthors": len(collaborators),
        "most_frequent_collaborators": frequent,
        "average_coauthors_per_paper": average_team_size,
        "recurring_collaboration_ratio": recurring_ratio,
        "team_structure": team_structure,
        "collaboration_diversity_score": diversity_score,
    }


def _parse_supervision_role(text: str) -> str:
    lowered = text.lower()
    if any(keyword in lowered for keyword in ROLE_KEYWORDS["co_supervisor"]):
        return "co-supervisor"
    if any(keyword in lowered for keyword in ROLE_KEYWORDS["main_supervisor"]):
        return "main-supervisor"
    return "unspecified"


def _parse_supervision_level(text: str) -> str:
    lowered = text.lower()
    if "phd" in lowered:
        return "PhD"
    if "ms" in lowered or "mphil" in lowered or "master" in lowered:
        return "MS"
    return "Unknown"


def _extract_year(text: str) -> int | None:
    match = re.search(r"(19|20)\d{2}", text)
    return int(match.group(0)) if match else None


def _extract_name_prefix(text: str) -> str:
    chunks = re.split(r"[-,:;]", text)
    for chunk in chunks:
        cleaned = _safe_name(chunk)
        if len(cleaned.split()) >= 2:
            return cleaned
    return ""


def analyze_supervision_profile(supervision: list[dict[str, Any]], publications: list[dict[str, Any]]) -> dict[str, Any]:
    parsed_entries = []
    supervised_names: set[str] = set()

    for entry in supervision:
        raw = entry.get("raw", "")
        role = _parse_supervision_role(raw)
        level = _parse_supervision_level(raw)
        year = _extract_year(raw)
        student = _extract_name_prefix(raw)
        if student:
            supervised_names.add(student)

        parsed_entries.append({
            "student": student,
            "level": level,
            "role": role,
            "graduation_year": year,
            "raw": raw,
        })

    main_supervisor_count = sum(1 for item in parsed_entries if item["role"] == "main-supervisor")
    co_supervisor_count = sum(1 for item in parsed_entries if item["role"] == "co-supervisor")

    papers_with_supervised_students = 0
    corresponding_author_count = 0
    for publication in publications:
        authors = [_safe_name(author) for author in publication.get("authors", []) if author]
        if supervised_names and any(name in supervised_names for name in authors):
            papers_with_supervised_students += 1
            if publication.get("candidate_authorship_role") in {"corresponding", "first_and_corresponding"}:
                corresponding_author_count += 1

    return {
        "total_supervised_students": len(parsed_entries),
        "main_supervisor_count": main_supervisor_count,
        "co_supervisor_count": co_supervisor_count,
        "papers_with_supervised_students": papers_with_supervised_students,
        "corresponding_papers_with_students": corresponding_author_count,
        "entries": parsed_entries,
    }


def _publisher_strength(publisher: str) -> str:
    lowered = (publisher or "").lower()
    if any(token in lowered for token in PUBLISHER_HINTS["strong"]):
        return "strong"
    if any(token in lowered for token in PUBLISHER_HINTS["moderate"]):
        return "moderate"
    if lowered:
        return "unknown"
    return "not-specified"


def analyze_books(books: list[dict[str, Any]], candidate_name: str) -> dict[str, Any]:
    candidate_norm = _safe_name(candidate_name)
    role_counts = Counter()

    for book in books:
        authors = [_safe_name(name) for name in book.get("authors", []) if name]
        if not authors:
            role = "unspecified"
        elif len(authors) == 1 and authors[0] == candidate_norm:
            role = "sole-author"
        elif authors and authors[0] == candidate_norm:
            role = "lead-author"
        elif candidate_norm in authors:
            role = "co-author"
        else:
            role = "contributor"

        book["candidate_role"] = role
        book["publisher_strength"] = _publisher_strength(book.get("publisher", ""))
        role_counts[role] += 1

    return {
        "total_books": len(books),
        "role_distribution": dict(role_counts),
        "books": books,
    }


def analyze_patents(patents: list[dict[str, Any]], candidate_name: str) -> dict[str, Any]:
    candidate_norm = _safe_name(candidate_name)
    role_counts = Counter()

    for patent in patents:
        inventors = [_safe_name(name) for name in patent.get("inventors", []) if name]
        if not inventors:
            role = "unspecified"
        elif inventors and inventors[0] == candidate_norm:
            role = "lead-inventor"
        elif candidate_norm in inventors:
            role = "co-inventor"
        else:
            role = "contributor"

        patent["candidate_role"] = role
        role_counts[role] += 1

    return {
        "total_patents": len(patents),
        "role_distribution": dict(role_counts),
        "patents": patents,
    }


def _skill_matches_text(skill: str, text: str) -> bool:
    return skill.lower() in (text or "").lower()


def analyze_skill_alignment(
    skills: list[str],
    experience: list[dict[str, Any]],
    publications: list[dict[str, Any]],
    topic_variability: dict[str, Any],
) -> dict[str, Any]:
    if not skills:
        return {
            "strongly_evidenced": [],
            "partially_evidenced": [],
            "weakly_evidenced": [],
            "unsupported": [],
            "alignment_score": 0.0,
        }

    experience_text = " ".join(
        f"{item.get('job_title', '')} {item.get('organization', '')} {item.get('raw', '')}" for item in experience
    )
    publication_text = " ".join(item.get("title", "") for item in publications)
    topic_text = " ".join(topic_variability.get("theme_distribution", {}).keys())

    strongly = []
    partial = []
    weak = []
    unsupported = []

    for skill in skills:
        in_experience = _skill_matches_text(skill, experience_text)
        in_research = _skill_matches_text(skill, publication_text) or _skill_matches_text(skill, topic_text)

        if in_experience and in_research:
            strongly.append(skill)
        elif in_experience or in_research:
            partial.append(skill)
        elif len(skill.strip()) <= 3:
            weak.append(skill)
        else:
            unsupported.append(skill)

    weighted_hits = len(strongly) * 1.0 + len(partial) * 0.6 + len(weak) * 0.3
    alignment_score = round((weighted_hits / len(skills)) * 100, 2) if skills else 0.0

    return {
        "strongly_evidenced": strongly,
        "partially_evidenced": partial,
        "weakly_evidenced": weak,
        "unsupported": unsupported,
        "alignment_score": alignment_score,
    }


def summarize_research_quality(publications: list[dict[str, Any]]) -> dict[str, Any]:
    if not publications:
        return {
            "indexed_publications": 0,
            "q1_q2_publications": 0,
            "conference_indexed": 0,
            "journal_indexed": 0,
            "quality_signal": "insufficient-data",
        }

    indexed_publications = 0
    q1_q2_publications = 0
    conference_indexed = 0
    journal_indexed = 0

    for publication in publications:
        api_info = publication.get("api_info", {}) or {}
        is_indexed = bool(api_info.get("is_indexed"))
        quartile = (api_info.get("inferred_quartile") or "Unknown").upper()
        pub_type = publication.get("type", "unknown")

        if is_indexed:
            indexed_publications += 1
            if pub_type == "conference":
                conference_indexed += 1
            if pub_type == "journal":
                journal_indexed += 1

        if quartile in {"Q1", "Q2"}:
            q1_q2_publications += 1

    indexed_ratio = indexed_publications / len(publications)
    if indexed_ratio >= 0.7 and q1_q2_publications >= max(1, len(publications) // 2):
        quality_signal = "strong"
    elif indexed_ratio >= 0.4:
        quality_signal = "moderate"
    else:
        quality_signal = "emerging"

    return {
        "indexed_publications": indexed_publications,
        "q1_q2_publications": q1_q2_publications,
        "conference_indexed": conference_indexed,
        "journal_indexed": journal_indexed,
        "quality_signal": quality_signal,
    }
