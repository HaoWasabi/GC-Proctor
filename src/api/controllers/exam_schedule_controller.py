from api.controllers.base_entity_controller import BaseEntityController
from models.exam_schedule_model import ExamScheduleModel
from services.exam_schedule_service import ExamScheduleService


class ExamScheduleController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=ExamScheduleService(),
            model_cls=ExamScheduleModel,
            entity_name="exam_schedule",
            get_one_method="get_exam_schedule",
            get_all_method="get_all_exam_schedules",
            create_method="create_exam_schedule",
            update_method="update_exam_schedule",
            delete_method="delete_exam_schedule",
            block_method="block_exam_schedule",
            unblock_method="unblock_exam_schedule",
        )