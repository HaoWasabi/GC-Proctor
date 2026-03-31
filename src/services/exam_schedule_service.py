from typing import List
from typing import Optional
from unittest import result

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
    
    def import_schedules_from_excel(self, file_path: str) -> str:
        return self.exam_schedule_repository.import_from_excel_batch(file_path)
    
# import os
# import pandas as pd
# from repositories.document_chunk_repository import DocumentChunkRepository

# def main():
#     # Khởi tạo repository
#     repo = ExamScheduleRepository()

#     # Sử dụng r"" để tránh lỗi đường dẫn Windows
#     excel_file_path = r"D:\do_an\AI\GC-Proctor\tmp\data_chunks.xlsx"

#     if not os.path.exists(excel_file_path):
#         print(f"Lỗi: Không tìm thấy file tại {excel_file_path}")
#         # Tự động tạo file mẫu nếu không tồn tại để bạn test
#         print("Đang tạo file mẫu để chạy thử...")
#         df_sample = pd.DataFrame([{
#             "examId": "EXAM001",
#             "studentId": "12345",
#             "examDate": "2024-12-01",
#             "startTime": "09:00",
#             "room": "A101",
#             "status": "1",
#             "updatedAt": "2024-05-20"


#         }])
#         df_sample.to_excel(excel_file_path, index=False, engine='openpyxl')

#     print(f"--- Bắt đầu Import từ: {excel_file_path} ---")

#     # Gọi hàm import
#     result = repo.import_schedules_from_excel(excel_file_path)

#     print("\n--- KẾT QUẢ ---")
#     print(f"Thành công: {result['success']}")
#     print(f"Thất bại:   {result['failed']}")

#     if result['errors']:
#         for err in result['errors']:
#             print(f"  - {err}")

# if __name__ == "__main__":
#     main()