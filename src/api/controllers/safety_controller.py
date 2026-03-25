from services.safety_service import SafetyService


class SafetyController:
    def __init__(self):
        self.service = SafetyService()

    def check_query(self, payload: dict) -> dict:
        return self.service.check_query(payload)

    def fallback_response(self, payload: dict) -> dict:
        return self.service.fallback_response(payload)

    def escalation_contacts(self) -> dict:
        return self.service.escalation_contacts()
