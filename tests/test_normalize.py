from app.normalize import normalize_candidate_id, normalize_phone, normalize_whitespace


def test_normalize_candidate_id() -> None:
    assert normalize_candidate_id("Dr. Jane Doe  ") == "dr_jane_doe"


def test_normalize_whitespace() -> None:
    assert normalize_whitespace("  a   b\t c  ") == "a b c"


def test_normalize_phone() -> None:
    assert normalize_phone("+92 300-123 4567") == "+923001234567"
