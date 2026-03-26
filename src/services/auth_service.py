from datetime import datetime
from datetime import timezone
from fastapi import HTTPException


class AuthService:
    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _extract_bearer(self, authorization: str | None) -> str:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="UNAUTHENTICATED")
        return authorization.split(" ", 1)[1]

    def login(self, payload: dict) -> dict:
        provider = payload.get("provider")
        identifier = payload.get("identifier")
        password = payload.get("password")

        if provider not in {"local", "sso"}:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: provider")
        if not identifier:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: identifier")
        if provider == "local" and not password:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: password")

        return {
            "accessToken": "access.mock.token",
            "refreshToken": "refresh.mock.token",
            "expiresIn": 3600,
            "tokenType": "Bearer",
            "user": {
                "id": "usr_demo",
                "userCode": identifier.upper(),
                "role": "student",
                "fullName": "Demo User",
                "email": "demo@example.edu",
                "authProvider": provider,
                "isActive": True,
            },
            "issuedAt": self._now(),
        }

    def refresh(self, payload: dict) -> dict:
        refresh_token = payload.get("refreshToken")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: refreshToken")

        return {
            "accessToken": "access.mock.token.refreshed",
            "expiresIn": 3600,
            "tokenType": "Bearer",
            "issuedAt": self._now(),
        }

    def me(self, authorization: str | None) -> dict:
        self._extract_bearer(authorization)
        return {
            "id": "usr_demo",
            "userCode": "SV00123",
            "role": "student",
            "fullName": "Demo User",
            "email": "demo@example.edu",
            "authProvider": "local",
            "createdAt": "2026-01-02T10:00:00Z",
            "updatedAt": "2026-03-10T07:30:00Z",
            "isActive": True,
        }

    def verify_student(self, payload: dict) -> dict:
        student_code = payload.get("studentCode")
        if not student_code:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: studentCode")

        return {
            "verified": True,
            "studentId": f"stu_{student_code.lower()}",
            "fullName": "Demo Student",
            "verificationLevel": "basic",
        }
