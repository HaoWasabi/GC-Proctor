from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.course_model import CourseModel
from .base_repository import BaseRepository, logger


class CourseRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "courses"

    def get_course(self, course_id: str) -> Optional[CourseModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(course_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return CourseModel(**doc_snapshot.to_dict())
            logger.warning(f"Course with ID {course_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching course {course_id}: {e}")
            return None

    def get_all_courses(self) -> List[CourseModel]:
        try:
            courses: List[CourseModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                courses.append(CourseModel(**doc.to_dict()))
            return courses
        except Exception as e:
            logger.error(f"Error fetching all courses: {e}")
            return []

    def create_course(self, course: CourseModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(course.get_id()).set(
                {
                    "id": course.get_id(),
                    "courseCode": course.get_courseCode(),
                    "courseName": course.get_courseName(),
                    "faculty": course.get_faculty(),
                    "semester": course.get_semester(),
                    "createdAt": course.get_createdAt(),
                    "isActive": course.get_state(),
                }
            )
            logger.info(f"Course {course.get_id()} created successfully.")
            return course.get_id()
        except Exception as e:
            logger.error(f"Error creating course {course.get_id()}: {e}")
            return None

    def update_course(self, course: CourseModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(course.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "courseCode": course.get_courseCode(),
                        "courseName": course.get_courseName(),
                        "faculty": course.get_faculty(),
                        "semester": course.get_semester(),
                        "createdAt": course.get_createdAt(),
                        "isActive": course.get_state(),
                    }
                )
                logger.info(f"Course {course.get_id()} updated successfully.")
                return True
            logger.warning(f"Course with ID {course.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating course {course.get_id()}: {e}")
            return False

    def delete_course(self, course_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(course_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Course {course_id} deleted successfully.")
                return True
            logger.warning(f"Course with ID {course_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting course {course_id}: {e}")
            return False

    def block_course(self, course_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(course_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Course {course_id} blocked successfully.")
                return True
            logger.warning(f"Course with ID {course_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking course {course_id}: {e}")
            return False

    def unblock_course(self, course_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(course_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Course {course_id} unblocked successfully.")
                return True
            logger.warning(f"Course with ID {course_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking course {course_id}: {e}")
            return False
