from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import Body

from api.controllers.nlp_controller import NLPController


router = APIRouter(prefix="/nlp", tags=["NLP"])
controller = NLPController()


def _ok(data: dict, request_id: str) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


@router.post("/parse-intent")
def parse_intent(payload: dict = Body(...)):
    return _ok(controller.parse_intent(payload), "req_nlp_parse_intent")


@router.post("/fallback-check")
def fallback_check(payload: dict = Body(...)):
    return _ok(controller.fallback_check(payload), "req_nlp_fallback_check")
