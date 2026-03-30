import os
import google.generativeai as genai
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

        # Cấu hình Gemini (Nên để API KEY trong file .env)
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

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
            """Truy vấn dữ liệu từ Firestore và chuyển thành văn bản ngữ cảnh"""
            schedules = self.schedule_repo.get_schedules_by_student(student_id)
            if not schedules:
                return "Không tìm thấy lịch thi."

            context_parts = []
            for s in schedules:
                exam = self.exam_repository.get_exam(s.get_examId())
                course_info = exam.get_courseId() if exam else "Môn học"
                info = f"- Môn: {course_info}, Ngày: {s.get_examDate()}, Phòng: {s.get_room()}, Giờ: {s.get_startTime()}"
                context_parts.append(info)
                
            return "\n".join(context_parts)

    def answer_exam_question(self, student_id: str, user_query: str):
        """Luồng RAG chính: Retrieval -> Augmentation -> Generation"""
        
        # 1. Retrieval: Lấy dữ liệu thực tế từ hệ thống
        context = self._get_raw_exam_data(student_id)
        
        # 2. Augmentation: Xây dựng Prompt với Persona thân thiện
        prompt = f"""
        Bạn là trợ lý ảo GC-Proctor, hỗ trợ sinh viên tra cứu lịch thi. 
        Hãy trả lời bằng giọng điệu thân thiện, hỗ trợ.

        Dữ liệu lịch thi hiện tại của sinh viên {student_id}:
        {context}

        Câu hỏi của sinh viên: "{user_query}"

        Yêu cầu:
        - Chỉ trả lời dựa trên dữ liệu được cung cấp.
        - Nếu không thấy thông tin, hãy hướng dẫn sinh viên liên hệ phòng đào tạo.
        - Định dạng câu trả lời rõ ràng, dễ nhìn.
        """

        # 3. Generation: Gọi Gemini để sinh câu trả lời
        response = self.model.generate_content(prompt)
        return response.text