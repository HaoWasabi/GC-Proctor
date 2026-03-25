from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import Body

from api.controllers.safety_controller import SafetyController


router = APIRouter(tags=["Safety"])
controller = SafetyController()


def _ok(data: dict, request_id: str) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


@router.post("/safety/check-query")
def check_query(payload: dict = Body(...)):
    return _ok(controller.check_query(payload), "req_safety_check_query")


@router.post("/fallback/respond")
def fallback_response(payload: dict = Body(...)):
    return _ok(controller.fallback_response(payload), "req_fallback_respond")


@router.get("/escalation/contacts")
def escalation_contacts():
    return _ok(controller.escalation_contacts(), "req_escalation_contacts")
