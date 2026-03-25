from services.exam_personalization_service import ExamPersonalizationService


class ExamPersonalizationController:
    def __init__(self):
        self.service = ExamPersonalizationService()

    def upcoming(self, days: int, status: str | None) -> dict:
        return self.service.upcoming(days=days, status=status)

    def today(self) -> dict:
        return self.service.today()

    def search(self, from_date: str, to_date: str, course_code: str | None, status: str | None) -> dict:
        return self.service.search(from_date, to_date, course_code, status)

    def next_exam(self) -> dict:
        return self.service.next_exam()
