from datetime import datetime, timezone
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from api.controllers.study_controller import StudyController


class QueryRequest(BaseModel):
    question: str = Field(..., description="Study question")
    course_id: Optional[str] = Field(None, description="Course ID (optional)")
    user_id: str = Field(..., description="User ID")


class SummarizeRequest(BaseModel):
    source: str = Field(..., description="Source material")
    source_type: str = Field("document", description="Type: document, course, or topic")
    length: str = Field("short", description="Summary length: short, medium, long")
    user_id: str = Field(..., description="User ID")


class FlashcardsRequest(BaseModel):
    topic: str = Field(..., description="Topic for flashcards")
    num_cards: int = Field(10, ge=1, le=100, description="Number of cards to generate")
    difficulty: str = Field("medium", description="Difficulty: easy, medium, hard")
    course_id: Optional[str] = Field(None, description="Course ID (optional)")
    user_id: str = Field(..., description="User ID")


class ExplainRequest(BaseModel):
    concept: str = Field(..., description="Concept to explain")
    level: str = Field("basic", description="Explanation level: basic, intermediate, advanced")
    user_id: str = Field(..., description="User ID")


router = APIRouter(prefix="/study", tags=["Study"])
controller = StudyController()


def _ok(data: dict, request_id: str) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


def _error(detail: str, status_code: int = 400) -> dict:
    raise HTTPException(status_code=status_code, detail=detail)


@router.post(
    "/query",
    summary="Query knowledge base for answers",
    description="Query the study knowledge base to get answers to study questions"
)
async def query(payload: QueryRequest) -> dict:
    """
    Query endpoint for studying.

    Request body:
    - question (required): The study question
    - user_id (required): User identifier
    - course_id (optional): Specific course to search within
    """
    try:
        result = controller.query(payload.dict())
        return _ok(result, "req_study_query")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in query: {e}")
        _error(f"Error processing query: {str(e)}", 500)


@router.post(
    "/summarize",
    summary="Summarize study materials",
    description="Generate summaries of study materials at various lengths"
)
async def summarize(payload: SummarizeRequest) -> dict:
    """
    Summarize endpoint for study materials.

    Request body:
    - source (required): The material to summarize
    - source_type (optional): Type of source - "document", "course", or "topic"
    - length (optional): Summary length - "short", "medium", or "long"
    - user_id (required): User identifier
    """
    try:
        result = controller.summarize(payload.dict())
        return _ok(result, "req_study_summarize")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in summarize: {e}")
        _error(f"Error processing summarize: {str(e)}", 500)


@router.post(
    "/flashcards/generate",
    summary="Generate flashcards for a topic",
    description="Automatically generate flashcards based on a topic"
)
async def generate_flashcards(payload: FlashcardsRequest) -> dict:
    """
    Generate flashcards endpoint.

    Request body:
    - topic (required): Topic for flashcard generation
    - num_cards (optional): Number of flashcards to generate (default: 10)
    - difficulty (optional): Difficulty level - "easy", "medium", or "hard"
    - course_id (optional): Specific course context
    - user_id (required): User identifier
    """
    try:
        result = controller.generate_flashcards(payload.dict())
        return _ok(result, "req_study_flashcards_generate")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in generate_flashcards: {e}")
        _error(f"Error processing flashcards: {str(e)}", 500)


@router.post(
    "/explain",
    summary="Get concept explanation at specified level",
    description="Get detailed explanations of concepts at different difficulty levels"
)
async def explain(payload: ExplainRequest) -> dict:
    """
    Explain concept endpoint.

    Request body:
    - concept (required): Concept to explain
    - level (optional): Explanation level - "basic", "intermediate", or "advanced"
    - user_id (required): User identifier
    """
    try:
        result = controller.explain(payload.dict())
        return _ok(result, "req_study_explain")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in explain: {e}")
        _error(f"Error processing explanation: {str(e)}", 500)


@router.get(
    "/history/{user_id}",
    summary="Get user's study history",
    description="Retrieve a user's study activity history"
)
async def get_study_history(
        user_id: str,
        limit: int = Field(50, ge=1, le=500)
) -> dict:
    """Get study history for a user"""
    try:
        history = controller.service.repository.get_user_study_history(user_id, limit)
        return _ok({"history": history, "total": len(history)}, "req_study_history")
    except Exception as e:
        print(f"Error in get_study_history: {e}")
        _error(f"Error retrieving history: {str(e)}", 500)


@router.get(
    "/flashcards/{user_id}",
    summary="Get user's flashcards",
    description="Retrieve a user's saved flashcards"
)
async def get_flashcards(
        user_id: str,
        topic: Optional[str] = Field(None, description="Filter by topic (optional)")
) -> dict:
    """Get flashcards for a user"""
    try:
        cards = controller.service.repository.get_user_flashcards(user_id, topic)
        return _ok({"flashcards": cards, "total": len(cards)}, "req_study_flashcards_list")
    except Exception as e:
        print(f"Error in get_flashcards: {e}")
        _error(f"Error retrieving flashcards: {str(e)}", 500)