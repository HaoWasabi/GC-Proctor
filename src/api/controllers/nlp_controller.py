from services.nlp_service import NLPService


class NLPController:
    def __init__(self):
        self.service = NLPService()

    def parse_intent(self, payload: dict) -> dict:
        return self.service.parse_intent(payload)

    def fallback_check(self, payload: dict) -> dict:
        return self.service.fallback_check(payload)
