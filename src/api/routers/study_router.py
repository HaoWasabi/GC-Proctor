from datetime import datetime, timezone
from fastapi import APIRouter, Body, Header
from api.controllers.study_orchestration_controller import StudyOrchestrationController


router = APIRouter(prefix="/study", tags=["Study"])
controller = StudyOrchestrationController()


def _ok(data: dict, request_id: str) -> dict:
    """Standardized response wrapper"""
    return {
        "success": True,
        "data": data,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


@router.post("/ask")
def ask_study_question(
    payload: dict = Body(...),
    authorization: str | None = Header(default=None, alias="Authorization")
):
    """Ask study-related questions - will infer course and retrieve materials"""
    result = controller.ask(payload)
    if result.get("success"):
        return _ok(result["data"], "req_study_ask")
    else:
        return {
            "success": False,
            "error": result.get("error"),
            "meta": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        }


@router.post("/flashcards/generate")
def generate_flashcards(payload: dict = Body(...)):
    """Generate flashcards for exam preparation"""
    result = controller.generate_flashcards(payload)
    if result.get("success"):
        return _ok(result["data"], "req_study_flashcards")
    else:
        return {
            "success": False,
            "error": result.get("error")
        }


@router.post("/material/summarize")
def summarize_material(payload: dict = Body(...)):
    """Summarize study materials for a course"""
    result = controller.summarize_material(payload)
    if result.get("success"):
        return _ok(result["data"], "req_study_summarize")
    else:
        return {
            "success": False,
            "error": result.get("error")
        }