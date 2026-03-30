from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.exam_schedule_model import ExamScheduleModel
from .base_repository import BaseRepository, logger


class ExamScheduleRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "exam_schedules"

    def get_exam_schedule(self, schedule_id: str) -> Optional[ExamScheduleModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(schedule_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return ExamScheduleModel(**doc_snapshot.to_dict())
            logger.warning(f"Exam schedule with ID {schedule_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching exam schedule {schedule_id}: {e}")
            return None

    def get_all_exam_schedules(self) -> List[ExamScheduleModel]:
        try:
            schedules: List[ExamScheduleModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                schedules.append(ExamScheduleModel(**doc.to_dict()))
            return schedules
        except Exception as e:
            logger.error(f"Error fetching all exam schedules: {e}")
            return []

    def create_exam_schedule(self, schedule: ExamScheduleModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(schedule.get_id()).set(
                {
                    "id": schedule.get_id(),
                    "examId": schedule.get_examId(),
                    "studentId": schedule.get_studentId(),
                    "examDate": schedule.get_examDate(),
                    "startTime": schedule.get_startTime(),
                    "room": schedule.get_room(),
                    "status": schedule.get_status(),
                    "updatedAt": schedule.get_updatedAt(),
                    "isActive": schedule.get_state(),
                }
            )
            logger.info(f"Exam schedule {schedule.get_id()} created successfully.")
            return schedule.get_id()
        except Exception as e:
            logger.error(f"Error creating exam schedule {schedule.get_id()}: {e}")
            return None

    def update_exam_schedule(self, schedule: ExamScheduleModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(schedule.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "examId": schedule.get_examId(),
                        "studentId": schedule.get_studentId(),
                        "examDate": schedule.get_examDate(),
                        "startTime": schedule.get_startTime(),
                        "room": schedule.get_room(),
                        "status": schedule.get_status(),
                        "updatedAt": schedule.get_updatedAt(),
                        "isActive": schedule.get_state(),
                    }
                )
                logger.info(f"Exam schedule {schedule.get_id()} updated successfully.")
                return True
            logger.warning(f"Exam schedule with ID {schedule.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating exam schedule {schedule.get_id()}: {e}")
            return False

    def delete_exam_schedule(self, schedule_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(schedule_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Exam schedule {schedule_id} deleted successfully.")
                return True
            logger.warning(f"Exam schedule with ID {schedule_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting exam schedule {schedule_id}: {e}")
            return False

    def block_exam_schedule(self, schedule_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(schedule_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Exam schedule {schedule_id} blocked successfully.")
                return True
            logger.warning(f"Exam schedule with ID {schedule_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking exam schedule {schedule_id}: {e}")
            return False

    def unblock_exam_schedule(self, schedule_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(schedule_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Exam schedule {schedule_id} unblocked successfully.")
                return True
            logger.warning(f"Exam schedule with ID {schedule_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking exam schedule {schedule_id}: {e}")
            return False

    def get_schedules_by_student(self, student_id: str) -> List[ExamScheduleModel]:
        try:
            schedules: List[ExamScheduleModel] = []
            # Truy vấn Firestore lọc theo studentId
            docs = self.db.collection(self.collection_name).where("studentId", "==", student_id).stream()
            for doc in docs:
                schedules.append(ExamScheduleModel(**doc.to_dict()))
            return schedules
        except Exception as e:
            logger.error(f"Error fetching schedules for student {student_id}: {e}")
            return []