from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.parser import parse_cv


@dataclass
class ProcessBatchResult:
    records: list[dict[str, Any]]
    failed_files: list[str]


def process_pdf_batch(pdf_paths: list[Path]) -> ProcessBatchResult:
    records: list[dict[str, Any]] = []
    failed_files: list[str] = []

    for pdf_path in pdf_paths:
        try:
            records.append(parse_cv(pdf_path))
        except Exception:
            failed_files.append(pdf_path.name)

    return ProcessBatchResult(records=records, failed_files=failed_files)
