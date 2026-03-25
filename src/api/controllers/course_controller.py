from api.controllers.base_entity_controller import BaseEntityController
from models.course_model import CourseModel
from services.course_service import CourseService


class CourseController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=CourseService(),
            model_cls=CourseModel,
            entity_name="course",
            get_one_method="get_course",
            get_all_method="get_all_courses",
            create_method="create_course",
            update_method="update_course",
            delete_method="delete_course",
            block_method="block_course",
            unblock_method="unblock_course",
        )