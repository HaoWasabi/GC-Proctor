from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import Body
from fastapi import Header
from fastapi import HTTPException
from fastapi import Query

from api.controllers.chat_orchestration_controller import ChatOrchestrationController


router = APIRouter(prefix="/chat", tags=["Chat"])
controller = ChatOrchestrationController()


def _ok(data: dict, request_id: str) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


def _require_auth(authorization: str | None) -> None:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="UNAUTHENTICATED")


@router.post("/ask")
def ask(
    payload: dict = Body(...),
    authorization: str | None = Header(default=None, alias="Authorization"),
):
    return _ok(controller.ask(payload, authorization), "req_chat_ask")


@router.post("/sessions/{session_id}/end")
def end_session(
    session_id: str,
    authorization: str | None = Header(default=None, alias="Authorization"),
):
    _require_auth(authorization)
    return _ok(controller.end_session(session_id), "req_chat_end_session")


@router.get("/sessions/{session_id}/context")
def get_context(
    session_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    beforeMessageId: str | None = Query(default=None),
    authorization: str | None = Header(default=None, alias="Authorization"),
):
    _require_auth(authorization)
    return _ok(controller.get_context(session_id, limit, beforeMessageId), "req_chat_context")
