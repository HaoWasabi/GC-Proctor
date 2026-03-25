from services.chat_orchestration_service import ChatOrchestrationService


class ChatOrchestrationController:
    def __init__(self):
        self.service = ChatOrchestrationService()

    def ask(self, payload: dict, authorization: str | None) -> dict:
        return self.service.ask(payload, authorization)

    def end_session(self, session_id: str) -> dict:
        return self.service.end_session(session_id)

    def get_context(self, session_id: str, limit: int, before_message_id: str | None) -> dict:
        return self.service.get_context(session_id, limit, before_message_id)
