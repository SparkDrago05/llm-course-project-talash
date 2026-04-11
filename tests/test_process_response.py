from app.schemas import ProcessResponse


def test_process_response_includes_failed_files_field() -> None:
    payload = ProcessResponse(
        processed_files=2,
        candidates=1,
        output_files=["data/output/candidates.csv"],
        failed_files=["broken.pdf"],
    )
    assert payload.failed_files == ["broken.pdf"]
