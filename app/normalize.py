import re


def normalize_candidate_id(raw: str) -> str:
    compact = re.sub(r"\s+", "_", raw.strip().lower())
    return re.sub(r"[^a-z0-9_]+", "", compact)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_phone(raw: str) -> str:
    value = re.sub(r"[^\d+]", "", raw)
    if value.startswith("++"):
        value = "+" + value.lstrip("+")
    return value
