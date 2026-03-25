from typing import List
from typing import Optional

from models.exam_model import ExamModel
from repositories.exam_repository import ExamRepository
from services.base_service import BaseService


class ExamService(BaseService):
    def __init__(self):
        super().__init__()
        self.exam_repository = ExamRepository()

    def get_exam(self, exam_id: str) -> Optional[ExamModel]:
        return self.exam_repository.get_exam(exam_id)

    def get_all_exams(self) -> List[ExamModel]:
        return self.exam_repository.get_all_exams()

    def create_exam(self, exam: ExamModel) -> Optional[str]:
        return self.exam_repository.create_exam(exam)

    def update_exam(self, exam: ExamModel) -> bool:
        return self.exam_repository.update_exam(exam)

    def delete_exam(self, exam_id: str) -> bool:
        return self.exam_repository.delete_exam(exam_id)

    def block_exam(self, exam_id: str) -> bool:
        return self.exam_repository.block_exam(exam_id)

    def unblock_exam(self, exam_id: str) -> bool:
        return self.exam_repository.unblock_exam(exam_id)