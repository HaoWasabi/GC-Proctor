from pydantic import BaseModel, Field
from typing import Optional, List
from services.study_service import StudyService
from fastapi import HTTPException

class QueryRequest(BaseModel):
    question: str
    course_id: Optional[str] = None
    user_id: str

class SummarizeRequest(BaseModel):
    source: str
    source_type: str = "document"  # document, course, topic
    length: str = "short"  # short, medium, long
    user_id: str

class FlashcardsRequest(BaseModel):
    topic: str
    course_id: Optional[str] = None
    num_cards: int = Field(default=10, ge=1, le=100)
    difficulty: str = "medium"
    user_id: str

class ExplainRequest(BaseModel):
    concept: str
    level: str = "basic"  # basic, intermediate, advanced
    user_id: str

class StudyController:
    def __init__(self):
        self.service = StudyService()

    def query(self, payload: QueryRequest) -> dict:
        return self.service.query(payload.dict())

    def summarize(self, payload: SummarizeRequest) -> dict:
        return self.service.summarize(payload.dict())

    def generate_flashcards(self, payload: FlashcardsRequest) -> dict:
        return self.service.generate_flashcards(payload.dict())

    def explain(self, payload: ExplainRequest) -> dict:
        return self.service.explain(payload.dict())

    def get_study_materials(self, payload: dict) -> dict:
        return self.service.get_study_materials(payload)