from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class Citation(BaseModel):
    chunk_id: str
    source: str
    text: str


class StudyLogModel(BaseModel):
    id: Optional[str] = None
    user_id: str
    question: Optional[str] = None
    answer: Optional[str] = None
    citations: Optional[List[Citation]] = []
    log_type: str = Field(default="query")  # query, summary, explanation
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True


class FlashcardModel(BaseModel):
    id: Optional[str] = None
    user_id: str
    topic: str
    front: str
    back: str
    difficulty: str = "medium"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    mastered: bool = False
    attempts: int = 0
    last_reviewed: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True