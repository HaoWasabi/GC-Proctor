from typing import List
from typing import Optional

from models.chat_session_model import ChatSessionModel
from repositories.chat_session_repository import ChatSessionRepository
from services.base_service import BaseService


class ChatSessionService(BaseService):
    def __init__(self):
        super().__init__()
        self.chat_session_repository = ChatSessionRepository()

    def get_chat_session(self, session_id: str) -> Optional[ChatSessionModel]:
        return self.chat_session_repository.get_chat_session(session_id)

    def get_all_chat_sessions(self) -> List[ChatSessionModel]:
        return self.chat_session_repository.get_all_chat_sessions()

    def create_chat_session(self, session: ChatSessionModel) -> Optional[str]:
        return self.chat_session_repository.create_chat_session(session)

    def update_chat_session(self, session: ChatSessionModel) -> bool:
        return self.chat_session_repository.update_chat_session(session)

    def delete_chat_session(self, session_id: str) -> bool:
        return self.chat_session_repository.delete_chat_session(session_id)

    def block_chat_session(self, session_id: str) -> bool:
        return self.chat_session_repository.block_chat_session(session_id)

    def unblock_chat_session(self, session_id: str) -> bool:
        return self.chat_session_repository.unblock_chat_session(session_id)