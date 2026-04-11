from pathlib import Path

from app.processor import process_pdf_batch


def test_process_pdf_batch_collects_failed_files(monkeypatch) -> None:
    paths = [Path("ok.pdf"), Path("bad.pdf")]

    def fake_parse(path: Path):
        if path.name == "bad.pdf":
            raise ValueError("parse failure")
        return {"candidate": {"candidate_id": "ok"}}

    monkeypatch.setattr("app.processor.parse_cv", fake_parse)

    result = process_pdf_batch(paths)
    assert len(result.records) == 1
    assert result.failed_files == ["bad.pdf"]
