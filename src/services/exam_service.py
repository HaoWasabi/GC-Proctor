from typing import List
from typing import Optional
from models.exam_model import ExamModel
from repositories.exam_schedule_repository import ExamScheduleRepository
from repositories.exam_repository import ExamRepository
from services.base_service import BaseService


class ExamService(BaseService):
    def __init__(self):
        super().__init__()
        self.exam_repository = ExamRepository()
        self.schedule_repo = ExamScheduleRepository()

    def get_exam(self, exam_id: str) -> Optional[ExamModel]:
        return self.exam_repository.get_exam(exam_id)

    def get_all_exams(self) -> List[ExamModel]:
        return self.exam_repository.get_all_exams()

    def create_exam(self, exam: ExamModel) -> Optional[str]:
        return self.exam_repository.create_exam(exam)

    def update_exam(self, exam: ExamModel) -> bool:
        return self.exam_repository.update_exam(exam)

    def delete_exam(self, exam_id: str) -> bool:
        return self.exam_repository.delete_exam(exam_id)

    def block_exam(self, exam_id: str) -> bool:
        return self.exam_repository.block_exam(exam_id)

    def unblock_exam(self, exam_id: str) -> bool:
        return self.exam_repository.unblock_exam(exam_id)
    
    def _get_raw_exam_data(self, student_id: str) -> str:
        schedules = self.schedule_repo.get_schedules_by_student(student_id)
        
        if not schedules:
            return "Không tìm thấy lịch thi."

        context_parts = []
        for s in schedules:
            exam = self.exam_repository.get_exam(s.get_examId())
            course_info = exam.get_courseId() if exam else "Môn học"
            info = f"- Môn: {course_info}, Ngày: {s.get_examDate()}, Phòng: {s.get_room()}, Giờ: {s.get_startTime()}, Trạng thái: {s.get_status()}"
            context_parts.append(info)
            
        return "\n".join(context_parts)

    def answer_exam_question(self, student_id: str, user_query: str):
        """Luồng RAG với Persona mạnh mẽ"""
        context = self._get_raw_exam_data(student_id)
        
        # Áp dụng tính cách GC-Proctor
        prompt = f"""
        Bạn là giám thị ảo GC-Proctor 🛡️. Nhiệm vụ của bạn là báo lịch thi.
        Dữ liệu lịch thi trong hệ thống của sinh viên mã {student_id}:
        {context}

        Câu hỏi của sinh viên: "{user_query}"

        Yêu cầu:
        - Báo lịch chính xác dựa trên Dữ liệu cung cấp. 
        - Giọng văn: Nghiêm túc nhưng thân thiện, xưng "mình", gọi sinh viên là "bạn". Có thể chúc thi tốt.
        - Nếu "Không tìm thấy lịch thi", hãy khuyên bạn ấy liên hệ phòng đào tạo.
        """

        response = self.model.generate_content(prompt)
        return response.text