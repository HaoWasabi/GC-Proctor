from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException
from fastapi import Query

from api.controllers.exam_personalization_controller import ExamPersonalizationController


router = APIRouter(prefix="/me", tags=["ExamSchedule"])
controller = ExamPersonalizationController()


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


@router.get("/exam-schedules/upcoming")
def upcoming(
    days: int = Query(default=14, ge=1, le=60),
    status: str | None = Query(default=None),
    authorization: str | None = Header(default=None, alias="Authorization"),
):
    _require_auth(authorization)
    return _ok(controller.upcoming(days, status), "req_me_exam_upcoming")


@router.get("/exam-schedules/today")
def today(authorization: str | None = Header(default=None, alias="Authorization")):
    _require_auth(authorization)
    return _ok(controller.today(), "req_me_exam_today")


@router.get("/exam-schedules")
def search(
    fromDate: str = Query(...),
    toDate: str = Query(...),
    courseCode: str | None = Query(default=None),
    status: str | None = Query(default=None),
    authorization: str | None = Header(default=None, alias="Authorization"),
):
    _require_auth(authorization)
    return _ok(controller.search(fromDate, toDate, courseCode, status), "req_me_exam_search")


@router.get("/exams/next")
def next_exam(authorization: str | None = Header(default=None, alias="Authorization")):
    _require_auth(authorization)
    return _ok(controller.next_exam(), "req_me_exam_next")
