
from typing import List
from typing import Optional

from models.chat_message_model import ChatMessageModel
from repositories.chat_message_repository import ChatMessageRepository
from services.base_service import BaseService


class ChatMessageService(BaseService):
    def __init__(self):
        super().__init__()
        self.chat_message_repository = ChatMessageRepository()

    def get_chat_message(self, message_id: str) -> Optional[ChatMessageModel]:
        return self.chat_message_repository.get_chat_message(message_id)

    def get_all_chat_messages(self) -> List[ChatMessageModel]:
        return self.chat_message_repository.get_all_chat_messages()

    def get_messages_by_session(self, session_id: str, limit: int = 50) -> List[ChatMessageModel]:
        return self.chat_message_repository.get_messages_by_session(session_id, limit)

    def create_chat_message(self, message: ChatMessageModel) -> Optional[str]:
        return self.chat_message_repository.create_chat_message(message)

    def update_chat_message(self, message: ChatMessageModel) -> bool:
        return self.chat_message_repository.update_chat_message(message)

    def delete_chat_message(self, message_id: str) -> bool:
        return self.chat_message_repository.delete_chat_message(message_id)

    def block_chat_message(self, message_id: str) -> bool:
        return self.chat_message_repository.block_chat_message(message_id)

    def unblock_chat_message(self, message_id: str) -> bool:
        return self.chat_message_repository.unblock_chat_message(message_id)
