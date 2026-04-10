from pathlib import Path
import pandas as pd

from app.config import (
    CANDIDATES_CSV,
    EDUCATION_CSV,
    EXPERIENCE_CSV,
    OUTPUT_DIR,
    PUBLICATIONS_CSV,
    SKILLS_CSV,
)


def _write_csv(path: Path, rows: list[dict]) -> None:
    frame = pd.DataFrame(rows)
    frame.to_csv(path, index=False)


def write_outputs(records: list[dict]) -> list[str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    candidates = [r["candidate"] for r in records]
    education = [item for r in records for item in r["education"]]
    experience = [item for r in records for item in r["experience"]]
    skills = [item for r in records for item in r["skills"]]
    publications = [item for r in records for item in r["publications"]]

    _write_csv(CANDIDATES_CSV, candidates)
    _write_csv(EDUCATION_CSV, education)
    _write_csv(EXPERIENCE_CSV, experience)
    _write_csv(SKILLS_CSV, skills)
    _write_csv(PUBLICATIONS_CSV, publications)

    return [
        str(CANDIDATES_CSV),
        str(EDUCATION_CSV),
        str(EXPERIENCE_CSV),
        str(SKILLS_CSV),
        str(PUBLICATIONS_CSV),
    ]
