from services.study_service import StudyService


class StudyController:
    def __init__(self):
        self.service = StudyService()

    def query(self, payload: dict) -> dict:
        return self.service.query(payload)

    def summarize(self, payload: dict) -> dict:
        return self.service.summarize(payload)

    def generate_flashcards(self, payload: dict) -> dict:
        return self.service.generate_flashcards(payload)

    def explain(self, payload: dict) -> dict:
        return self.service.explain(payload)
