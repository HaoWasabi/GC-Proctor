from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import Body
from fastapi import Header

from api.controllers.auth_controller import AuthController


router = APIRouter(prefix="/auth", tags=["Auth"])
controller = AuthController()


def _ok(data: dict, request_id: str) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": {
            "requestId": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


@router.post("/login")
def login(payload: dict = Body(...)):
    return _ok(controller.login(payload), "req_auth_login")


@router.post("/refresh")
def refresh(payload: dict = Body(...)):
    return _ok(controller.refresh(payload), "req_auth_refresh")


@router.get("/me")
def me(authorization: str | None = Header(default=None, alias="Authorization")):
    return _ok(controller.me(authorization), "req_auth_me")


@router.post("/verify-student")
def verify_student(payload: dict = Body(...)):
    return _ok(controller.verify_student(payload), "req_auth_verify_student")
