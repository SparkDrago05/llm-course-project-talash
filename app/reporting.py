from pathlib import Path
import pandas as pd


def _load(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def build_preprocessing_report(output_dir: Path) -> dict:
    candidates = _load(output_dir / "candidates.csv")
    education = _load(output_dir / "education.csv")
    experience = _load(output_dir / "experience.csv")
    skills = _load(output_dir / "skills.csv")
    publications = _load(output_dir / "publications.csv")
    supervision = _load(output_dir / "supervision.csv")
    patents = _load(output_dir / "patents.csv")
    books = _load(output_dir / "books.csv")

    if candidates.empty:
        return {
            "candidates": 0,
            "table_rows": {},
            "completeness": {},
        }

    total = len(candidates)
    table_rows = {
        "education": len(education),
        "experience": len(experience),
        "skills": len(skills),
        "publications": len(publications),
        "supervision": len(supervision),
        "patents": len(patents),
        "books": len(books),
    }

    per_candidate = {
        "education": education["candidate_id"].nunique() if not education.empty else 0,
        "experience": experience["candidate_id"].nunique() if not experience.empty else 0,
        "skills": skills["candidate_id"].nunique() if not skills.empty else 0,
        "publications": publications["candidate_id"].nunique() if not publications.empty else 0,
        "supervision": supervision["candidate_id"].nunique() if not supervision.empty else 0,
        "patents": patents["candidate_id"].nunique() if not patents.empty else 0,
        "books": books["candidate_id"].nunique() if not books.empty else 0,
    }

    completeness = {
        key: round((value / total) * 100, 2) if total else 0.0
        for key, value in per_candidate.items()
    }

    return {
        "candidates": total,
        "table_rows": table_rows,
        "completeness": completeness,
    }
