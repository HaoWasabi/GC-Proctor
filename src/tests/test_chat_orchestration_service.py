import unittest
from unittest.mock import patch

from services.chat_orchestration_service import ChatOrchestrationService


class TestChatOrchestrationService(unittest.TestCase):
    def setUp(self):
        self.patcher_nlp = patch("services.chat_orchestration_service.NLPService")
        self.patcher_study = patch("services.chat_orchestration_service.StudyService")
        self.patcher_user = patch("services.chat_orchestration_service.UserService")
        self.patcher_exam = patch("services.chat_orchestration_service.ExamService")
        self.patcher_exam_schedule = patch("services.chat_orchestration_service.ExamScheduleService")
        self.patcher_regulation = patch("services.chat_orchestration_service.RegulationService")
        self.patcher_help = patch("services.chat_orchestration_service.HelpRequestService")

        self.mock_nlp_cls = self.patcher_nlp.start()
        self.mock_study_cls = self.patcher_study.start()
        self.mock_user_cls = self.patcher_user.start()
        self.mock_exam_cls = self.patcher_exam.start()
        self.mock_exam_schedule_cls = self.patcher_exam_schedule.start()
        self.mock_regulation_cls = self.patcher_regulation.start()
        self.mock_help_cls = self.patcher_help.start()

        self.service = ChatOrchestrationService()

    def tearDown(self):
        self.patcher_nlp.stop()
        self.patcher_study.stop()
        self.patcher_user.stop()
        self.patcher_exam.stop()
        self.patcher_exam_schedule.stop()
        self.patcher_regulation.stop()
        self.patcher_help.stop()

    def test_exam_schedule_intent_routes_to_exam_service(self):
        self.mock_nlp_cls.return_value.parse_intent.return_value = {"intent": "exam_schedule"}
        self.mock_exam_cls.return_value.answer_exam_question.return_value = "Bạn thi lúc 08:00 tại A102"

        result = self.service.ask({"question": "Lịch thi của mình", "userId": "SV001"})

        self.mock_exam_cls.return_value.answer_exam_question.assert_called_once_with("SV001", "Lịch thi của mình")
        self.assertEqual(result["intent"], "exam_schedule")
        self.assertEqual(result["answer"]["text"], "Bạn thi lúc 08:00 tại A102")

    def test_study_support_uses_upcoming_exams(self):
        self.mock_nlp_cls.return_value.parse_intent.return_value = {"intent": "study_support"}
        self.mock_user_cls.return_value.get_user.return_value = {"id": "SV001"}
        self.mock_exam_schedule_cls.return_value.get_upcoming_exams.return_value = [
            {"examId": "EX1", "examDate": "2026-04-01"}
        ]
        self.mock_study_cls.return_value.process_study_workflow.return_value = {
            "answer": "Nên ôn CTDL trước.",
            "citations": [],
            "metadata": {"course_code": "CS101"},
        }

        result = self.service.ask({"question": "Gợi ý ôn tập", "userId": "SV001"})

        self.mock_exam_schedule_cls.return_value.get_upcoming_exams.assert_called_once_with("SV001")
        self.mock_study_cls.return_value.process_study_workflow.assert_called_once()
        self.assertEqual(result["intent"], "study_support")
        self.assertEqual(result["answer"], "Nên ôn CTDL trước.")


if __name__ == "__main__":
    unittest.main()
