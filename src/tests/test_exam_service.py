import unittest
from unittest.mock import MagicMock, patch
from services.exam_service import ExamService
from models.exam_schedule_model import ExamScheduleModel
from models.exam_model import ExamModel
from datetime import date

class TestExamService(unittest.TestCase):

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def setUp(self, mock_model, mock_configure):
        # Giả lập ExamRepository và ExamScheduleRepository
        self.patcher_schedule_repo = patch('services.exam_service.ExamScheduleRepository')
        self.patcher_exam_repo = patch('services.exam_service.ExamRepository')
        
        self.mock_schedule_repo = self.patcher_schedule_repo.start()
        self.mock_exam_repo = self.patcher_exam_repo.start()
        
        # Khởi tạo service (lúc này các repo đã bị mock)
        self.exam_service = ExamService()
        
        # Giả lập đối tượng Gemini model
        self.mock_gemini = MagicMock()
        self.exam_service.model = self.mock_gemini

    def tearDown(self):
        self.patcher_schedule_repo.stop()
        self.patcher_exam_repo.stop()

    def test_answer_exam_question_success(self):
        # 1. Chuẩn bị dữ liệu mẫu (Mock Data)
        student_id = "SV001"
        user_query = "Ngày mai mình thi ở đâu?"
        
        # Tạo mock schedule
        mock_schedule = MagicMock(spec=ExamScheduleModel)
        mock_schedule.get_examId.return_value = "EXAM_01"
        mock_schedule.get_examDate.return_value = "2026-04-01"
        mock_schedule.get_room.return_value = "A102"
        mock_schedule.get_startTime.return_value = "08:00"
        
        # Tạo mock exam detail
        mock_exam = MagicMock(spec=ExamModel)
        mock_exam.get_courseId.return_value = "CS101 - Lập trình Python"

        # Cấu hình trả về cho các hàm mock repo
        self.mock_schedule_repo.return_value.get_schedules_by_student.return_value = [mock_schedule]
        self.mock_exam_repo.return_value.get_exam.return_value = mock_exam
        
        # Giả lập phản hồi từ Gemini
        mock_response = MagicMock()
        mock_response.text = "Bạn có lịch thi môn Lập trình Python vào ngày 01/04/2026 tại phòng A102 lúc 08:00 nhé."
        self.mock_gemini.generate_content.return_value = mock_response

        # 2. Thực thi hàm cần test
        result = self.exam_service.answer_exam_question(student_id, user_query)

        # 3. Kiểm chứng (Assertions)
        # Kiểm tra xem repo có được gọi đúng student_id không
        self.mock_schedule_repo.return_value.get_schedules_by_student.assert_called_once_with(student_id)
        
        # Kiểm tra xem Gemini có được gọi không
        self.assertTrue(self.mock_gemini.generate_content.called)
        
        # Kiểm tra kết quả trả về
        self.assertEqual(result, mock_response.text)
        print("\nTest Success: Trả về câu trả lời đúng ngữ cảnh.")

    def test_answer_exam_question_no_data(self):
        # Giả lập trường hợp sinh viên không có lịch thi
        student_id = "SV999"
        self.mock_schedule_repo.return_value.get_schedules_by_student.return_value = []
        
        mock_response = MagicMock()
        mock_response.text = "Hiện tại mình không tìm thấy lịch thi nào của bạn."
        self.mock_gemini.generate_content.return_value = mock_response

        result = self.exam_service.answer_exam_question(student_id, "Lịch thi của mình đâu?")

        self.assertIn("không tìm thấy", result)
        print("Test No Data: Xử lý tốt khi database trống.")
        print("Câu trả lời:", result)

if __name__ == '__main__':
    unittest.main()