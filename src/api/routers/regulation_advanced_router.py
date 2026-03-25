from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import Body

from api.controllers.regulation_advanced_controller import RegulationAdvancedController


router = APIRouter(prefix="/regulations", tags=["Regulations"])
controller = RegulationAdvancedController()


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
    return _ok(controller.query(payload), "req_regulations_query")


@router.get("/{regulation_id}/clauses")
def get_clauses(regulation_id: str):
    return _ok(controller.get_clauses(regulation_id), "req_regulations_clauses")


@router.post("/validate-answer")
def validate_answer(payload: dict = Body(...)):
    return _ok(controller.validate_answer(payload), "req_regulations_validate_answer")
