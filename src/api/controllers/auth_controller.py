from services.auth_service import AuthService


class AuthController:
    def __init__(self):
        self.service = AuthService()

    def login(self, payload: dict) -> dict:
        return self.service.login(payload)

    def refresh(self, payload: dict) -> dict:
        return self.service.refresh(payload)

    def me(self, authorization: str | None) -> dict:
        return self.service.me(authorization)

    def verify_student(self, payload: dict) -> dict:
        return self.service.verify_student(payload)
