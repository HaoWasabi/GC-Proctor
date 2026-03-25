from typing import List
from typing import Optional

from models.course_model import CourseModel
from repositories.course_repository import CourseRepository
from services.base_service import BaseService


class CourseService(BaseService):
    def __init__(self):
        super().__init__()
        self.course_repository = CourseRepository()

    def get_course(self, course_id: str) -> Optional[CourseModel]:
        return self.course_repository.get_course(course_id)

    def get_all_courses(self) -> List[CourseModel]:
        return self.course_repository.get_all_courses()

    def create_course(self, course: CourseModel) -> Optional[str]:
        return self.course_repository.create_course(course)

    def update_course(self, course: CourseModel) -> bool:
        return self.course_repository.update_course(course)

    def delete_course(self, course_id: str) -> bool:
        return self.course_repository.delete_course(course_id)

    def block_course(self, course_id: str) -> bool:
        return self.course_repository.block_course(course_id)

    def unblock_course(self, course_id: str) -> bool:
        return self.course_repository.unblock_course(course_id)