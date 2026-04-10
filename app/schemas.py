from typing import List
from pydantic import BaseModel


class IngestResponse(BaseModel):
    file_name: str
    saved_to: str


class CandidateSummary(BaseModel):
    candidate_id: str
    name: str
    email: str
    phone: str
    current_title: str


class ProcessResponse(BaseModel):
    processed_files: int
    candidates: int
    output_files: List[str]
