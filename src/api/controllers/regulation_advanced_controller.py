from services.regulation_advanced_service import RegulationAdvancedService


class RegulationAdvancedController:
    def __init__(self):
        self.service = RegulationAdvancedService()

    def query(self, payload: dict) -> dict:
        return self.service.query(payload)

    def get_clauses(self, regulation_id: str) -> dict:
        return self.service.get_clauses(regulation_id)

    def validate_answer(self, payload: dict) -> dict:
        return self.service.validate_answer(payload)
