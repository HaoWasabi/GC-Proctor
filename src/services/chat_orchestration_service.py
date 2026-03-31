from services.nlp_service import NLPService
from services.study_service import StudyService
from services.user_service import UserService
from services.exam_schedule_service import ExamScheduleService
from services.help_request_service import HelpRequestService


class ChatOrchestrationService:
    """SIMPLIFIED - Routes user queries to appropriate service"""

    def __init__(self):
        self.nlp_service = NLPService()
        self.study_service = StudyService()
        self.user_service = UserService()
        self.exam_schedule_service = ExamScheduleService()
        self.help_request_service = HelpRequestService()

    def ask(self, payload: dict, authorization: str = None) -> dict:
        """Handle user question and route to appropriate service"""

        question = payload.get("question", "")
        user_id = payload.get("userId", "default_user")

        # Parse intent
        intent_result = self.nlp_service.parse_intent(question)
        intent = intent_result.get("intent")

        # Route to appropriate service
        if intent == "help_request":
            # Route to help request service
            result = self.help_request_service.create_help_session(user_id, question)
            return {
                "intent": "help_request",
                "sessionId": result.get("sessionId"),
                "channel": result.get("channel"),
                "botResponse": result.get("botResponse"),
                "timestamp": result.get("timestamp")
            }
        
        elif intent == "study_support":
            # Get user context
            try:
                user_info = self.user_service.get_user(user_id)
                upcoming_exams = self.exam_schedule_service.get_upcoming_exams(user_id)
            except:
                user_info = {}
                upcoming_exams = []

            # Process with study service
            result = self.study_service.process_study_workflow(question, user_info, upcoming_exams)

            return {
                "intent": "study_support",
                "answer": result.get("answer"),
                "citations": result.get("citations"),
                "metadata": result.get("metadata")
            }
        
        else:
            return {
                "intent": intent,
                "answer": {"text": "Câu hỏi này không được hỗ trợ. Vui lòng hỏi về ôn tập hoặc yêu cầu trợ giúp."},
                "citations": []
            }
