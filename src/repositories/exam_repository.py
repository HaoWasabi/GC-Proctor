from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.exam_model import ExamModel
from .base_repository import BaseRepository, logger


class ExamRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "exams"

    def get_exam(self, exam_id: str) -> Optional[ExamModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(exam_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return ExamModel(**doc_snapshot.to_dict())
            logger.warning(f"Exam with ID {exam_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching exam {exam_id}: {e}")
            return None

    def get_all_exams(self) -> List[ExamModel]:
        try:
            exams: List[ExamModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                exams.append(ExamModel(**doc.to_dict()))
            return exams
        except Exception as e:
            logger.error(f"Error fetching all exams: {e}")
            return []

    def create_exam(self, exam: ExamModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(exam.get_id()).set(
                {
                    "id": exam.get_id(),
                    "courseId": exam.get_courseId(),
                    "examType": exam.get_examType(),
                    "durationMinutes": exam.get_durationMinutes(),
                    "policyVersion": exam.get_policyVersion(),
                    "createdAt": exam.get_createdAt(),
                    "isActive": exam.get_state(),
                }
            )
            logger.info(f"Exam {exam.get_id()} created successfully.")
            return exam.get_id()
        except Exception as e:
            logger.error(f"Error creating exam {exam.get_id()}: {e}")
            return None

    def update_exam(self, exam: ExamModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(exam.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "courseId": exam.get_courseId(),
                        "examType": exam.get_examType(),
                        "durationMinutes": exam.get_durationMinutes(),
                        "policyVersion": exam.get_policyVersion(),
                        "createdAt": exam.get_createdAt(),
                        "isActive": exam.get_state(),
                    }
                )
                logger.info(f"Exam {exam.get_id()} updated successfully.")
                return True
            logger.warning(f"Exam with ID {exam.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating exam {exam.get_id()}: {e}")
            return False

    def delete_exam(self, exam_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(exam_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Exam {exam_id} deleted successfully.")
                return True
            logger.warning(f"Exam with ID {exam_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting exam {exam_id}: {e}")
            return False

    def block_exam(self, exam_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(exam_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Exam {exam_id} blocked successfully.")
                return True
            logger.warning(f"Exam with ID {exam_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking exam {exam_id}: {e}")
            return False

    def unblock_exam(self, exam_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(exam_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Exam {exam_id} unblocked successfully.")
                return True
            logger.warning(f"Exam with ID {exam_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking exam {exam_id}: {e}")
            return False
