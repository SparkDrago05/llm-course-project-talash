from pathlib import Path

from app.reporting import build_preprocessing_report


def test_build_preprocessing_report_with_no_candidates(tmp_path: Path) -> None:
    report = build_preprocessing_report(tmp_path)
    assert report["candidates"] == 0
    assert report["table_rows"] == {}
    assert report["completeness"] == {}
