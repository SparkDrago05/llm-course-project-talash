from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
CANDIDATES_CSV = OUTPUT_DIR / "candidates.csv"
EDUCATION_CSV = OUTPUT_DIR / "education.csv"
EXPERIENCE_CSV = OUTPUT_DIR / "experience.csv"
SKILLS_CSV = OUTPUT_DIR / "skills.csv"
PUBLICATIONS_CSV = OUTPUT_DIR / "publications.csv"
SUPERVISION_CSV = OUTPUT_DIR / "supervision.csv"
PATENTS_CSV = OUTPUT_DIR / "patents.csv"
BOOKS_CSV = OUTPUT_DIR / "books.csv"


def ensure_directories() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
