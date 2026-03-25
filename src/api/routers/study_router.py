from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import Body

from api.controllers.study_controller import StudyController


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


@router.post("/query")
def query(payload: dict = Body(...)):
    return _ok(controller.query(payload), "req_study_query")


@router.post("/summarize")
def summarize(payload: dict = Body(...)):
    return _ok(controller.summarize(payload), "req_study_summarize")


@router.post("/flashcards/generate")
def generate_flashcards(payload: dict = Body(...)):
    return _ok(controller.generate_flashcards(payload), "req_study_flashcards_generate")


@router.post("/explain")
def explain(payload: dict = Body(...)):
    return _ok(controller.explain(payload), "req_study_explain")
