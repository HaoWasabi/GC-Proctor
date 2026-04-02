from datetime import datetime
import openpyxl
from typing import List, Optional
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1 import DocumentSnapshot
from models.exam_schedule_model import ExamScheduleModel
from repositories.user_repository import UserRepository
from .base_repository import BaseRepository, logger


class ExamScheduleRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "exam_schedules"
        self.user_repository = UserRepository()

    def get_exam_schedule(self, schedule_id: str) -> Optional[ExamScheduleModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(schedule_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                data = doc_snapshot.to_dict()
                data['id'] = data.get('id', doc_snapshot.id)
                return ExamScheduleModel(**data)
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
                data = doc.to_dict()
                data['id'] = data.get('id', doc.id)
                schedules.append(ExamScheduleModel(**data))
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

            normalized_student_id = str(student_id or "").strip()
            student_id_candidates = [normalized_student_id]

            matched_user = self.user_repository.get_user_by_userCode(normalized_student_id)
            if matched_user:
                student_id_candidates.append(str(matched_user.get_id()).strip())

            seen_schedule_ids = set()
            for candidate in student_id_candidates:
                if not candidate:
                    continue

                docs = self.db.collection(self.collection_name).where(filter=FieldFilter("studentId", "==", candidate)).stream()
                for doc in docs:
                    data = doc.to_dict()
                    data['id'] = data.get('id', doc.id)
                    if data['id'] in seen_schedule_ids:
                        continue
                    schedules.append(ExamScheduleModel(**data))
                    seen_schedule_ids.add(data['id'])

            if schedules:
                return schedules

            # Fallback sâu hơn: quét toàn bộ bản ghi để hỗ trợ dữ liệu cũ/lệch schema
            for doc in self.db.collection(self.collection_name).stream():
                data = doc.to_dict()
                data['id'] = data.get('id', doc.id)
                stored_student_id = str(data.get("studentId") or data.get("student_id") or "").strip()
                if stored_student_id in student_id_candidates:
                    if data['id'] in seen_schedule_ids:
                        continue
                    schedules.append(ExamScheduleModel(**data))
                    seen_schedule_ids.add(data['id'])

            return schedules
        except Exception as e:
            logger.error(f"Error fetching schedules for student {student_id}: {e}")
            return []
            
    def import_schedules_from_excel(self, file_path: str):
        try:
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active
            
            batch = self.get_batch()
            count = 0

            # Cấu trúc file Excel giả định: 
            # A: StudentID, B: ExamID, C: Date, D: Time, E: Room
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row[0]: continue
                
                # Tạo ID duy nhất để tránh trùng lặp: studentId_examId
                custom_id = f"{row[0]}_{row[1]}"
                doc_ref = self.db.collection(self.collection_name).document(custom_id)
                
                batch.set(doc_ref, {
                    "id": custom_id,
                    "studentId": str(row[0]),
                    "examId": str(row[1]),
                    "examDate": row[2], # openpyxl tự convert sang datetime nếu cell định dạng date
                    "startTime": str(row[3]),
                    "room": str(row[4]),
                    "status": "scheduled",
                    "updatedAt": str(datetime.now()),
                    "isActive": True
                })
                
                count += 1
                if count % 500 == 0:
                    batch.commit()
                    batch = self.get_batch()

            batch.commit()
            return {"success": 1, "failed": 0, "errors": []}
        except Exception as e:
            logger.error(f"Error importing exam schedules from Excel: {e}")
            return {"success": 0, "failed": 0, "errors": [str(e)]}