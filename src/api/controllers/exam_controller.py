from api.controllers.base_entity_controller import BaseEntityController
from models.exam_model import ExamModel
from services.exam_service import ExamService


class ExamController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=ExamService(),
            model_cls=ExamModel,
            entity_name="exam",
            get_one_method="get_exam",
            get_all_method="get_all_exams",
            create_method="create_exam",
            update_method="update_exam",
            delete_method="delete_exam",
            block_method="block_exam",
            unblock_method="unblock_exam",
            answer_exam_question_method="answer_exam_question"
        )