from fastapi import HTTPException
from services.nlp_service import NLPService
from services.study_service import StudyService
from services.user_service import UserService
from services.exam_schedule_service import ExamScheduleService


class ChatOrchestrationService:
    def __init__(self):
        self.nlp_service = NLPService()
        self.study_service = StudyService()
        self.user_service = UserService()
        self.exam_schedule_service = ExamScheduleService()

    def ask(self, payload: dict, authorization: str | None) -> dict:
        question = payload.get("question", "")

        intent_result = self.nlp_service.parse_intent({"question": question, "entities": payload.get("context", {})})
        intent_name = intent_result.get("intent")

        answer_text = ""
        citations = []

        if intent_name == "study_support":
            # BƯỚC 0: Tận dụng hàm sẵn có lấy thông tin user và lịch thi
            user_id = payload.get("context", {}).get("userId", "default_user")  # Lấy từ token/payload

            try:
                # Gọi hàm có sẵn trong user_service và exam_schedule_service
                user_info = self.user_service.get_user(user_id)
                # Lấy tất cả lịch thi hoặc lịch thi sắp tới từ DB
                upcoming_exams = self.exam_schedule_service.get_upcoming_exams(user_id)
            except Exception as e:
                user_info = {}
                upcoming_exams = []

            # Chuyển toàn bộ dữ liệu (câu hỏi, info, lịch thi) sang Study Service để xử lý RAG
            study_result = self.study_service.process_study_workflow(
                question=question,
                user_info=user_info,
                upcoming_exams=upcoming_exams
            )

            answer_text = study_result["answer"]
            citations = study_result["citations"]

        else:
            answer_text = "Câu hỏi của bạn không thuộc luồng ôn tập."

        return {
            "intent": intent_name,
            "answer": {"text": answer_text},
            "citations": citations
        }

    def end_session(self, session_id: str) -> dict:
        if not session_id:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: session_id")

        return {
            "sessionId": session_id,
            "sessionStatus": "closed",
            "endedAt": "2026-03-25T10:40:00Z",
        }

    def get_context(self, session_id: str, limit: int, before_message_id: str | None) -> dict:
        if not session_id:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: session_id")

        return {
            "session": {
                "id": session_id,
                "userId": "usr_demo",
                "channel": "web",
                "persona": "friendly",
                "sessionStatus": "active",
                "startedAt": "2026-03-25T10:00:00Z",
                "endedAt": None,
                "isActive": True,
            },
            "messages": [
                {
                    "id": before_message_id or "msg_user_001",
                    "senderType": "user",
                    "intent": "unknown",
                    "content": "Cho minh hoi...",
                    "citations": [],
                    "entities": {},
                    "createdAt": "2026-03-25T10:01:00Z",
                    "isActive": True,
                }
            ][: max(1, min(limit, 100))],
        }
