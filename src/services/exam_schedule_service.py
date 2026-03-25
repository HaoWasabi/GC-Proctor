from typing import List
from typing import Optional

from models.exam_schedule_model import ExamScheduleModel
from repositories.exam_schedule_repository import ExamScheduleRepository
from services.base_service import BaseService


class ExamScheduleService(BaseService):
    def __init__(self):
        super().__init__()
        self.exam_schedule_repository = ExamScheduleRepository()

    def get_exam_schedule(self, schedule_id: str) -> Optional[ExamScheduleModel]:
        return self.exam_schedule_repository.get_exam_schedule(schedule_id)

    def get_all_exam_schedules(self) -> List[ExamScheduleModel]:
        return self.exam_schedule_repository.get_all_exam_schedules()

    def create_exam_schedule(self, schedule: ExamScheduleModel) -> Optional[str]:
        return self.exam_schedule_repository.create_exam_schedule(schedule)

    def update_exam_schedule(self, schedule: ExamScheduleModel) -> bool:
        return self.exam_schedule_repository.update_exam_schedule(schedule)

    def delete_exam_schedule(self, schedule_id: str) -> bool:
        return self.exam_schedule_repository.delete_exam_schedule(schedule_id)

    def block_exam_schedule(self, schedule_id: str) -> bool:
        return self.exam_schedule_repository.block_exam_schedule(schedule_id)

    def unblock_exam_schedule(self, schedule_id: str) -> bool:
        return self.exam_schedule_repository.unblock_exam_schedule(schedule_id)