from typing import List, Optional
from datetime import datetime, timezone
from google.cloud.firestore_v1 import DocumentSnapshot
from models.chat_message_model import ChatMessageModel
from .base_repository import BaseRepository, logger


class ChatMessageRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "chat_messages"

    def get_chat_message(self, message_id: str) -> Optional[ChatMessageModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(message_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return ChatMessageModel(**doc_snapshot.to_dict())
            logger.warning(f"Chat message with ID {message_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching chat message {message_id}: {e}")
            return None

    def get_all_chat_messages(self) -> List[ChatMessageModel]:
        try:
            messages: List[ChatMessageModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                messages.append(ChatMessageModel(**doc.to_dict()))
            return messages
        except Exception as e:
            logger.error(f"Error fetching all chat messages: {e}")
            return []

    def get_messages_by_session(self, session_id: str, limit: int = 50) -> List[ChatMessageModel]:
        try:
            messages: List[ChatMessageModel] = []
            query = self.db.collection(self.collection_name).where("sessionId", "==", session_id)
            for doc in query.stream():
                messages.append(ChatMessageModel(**doc.to_dict()))

            def _normalize_created_at(value):
                if value is None:
                    return datetime(1970, 1, 1, tzinfo=timezone.utc)
                if isinstance(value, datetime):
                    if value.tzinfo is None:
                        return value.replace(tzinfo=timezone.utc)
                    return value
                try:
                    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
                    if parsed.tzinfo is None:
                        return parsed.replace(tzinfo=timezone.utc)
                    return parsed
                except Exception:
                    return datetime(1970, 1, 1, tzinfo=timezone.utc)

            messages.sort(key=lambda m: _normalize_created_at(m.get_createdAt()))
            if limit and limit > 0:
                return messages[-limit:]
            return messages
        except Exception as e:
            logger.error(f"Error fetching messages for session {session_id}: {e}")
            return []

    def create_chat_message(self, message: ChatMessageModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(message.get_id()).set(
                {
                    "id": message.get_id(),
                    "sessionId": message.get_sessionId(),
                    "senderType": message.get_senderType(),
                    "intent": message.get_intent(),
                    "content": message.get_content(),
                    "citations": message.get_citations(),
                    "entities": message.get_entities(),
                    "createdAt": message.get_createdAt(),
                    "isActive": message.get_state(),
                }
            )
            logger.info(f"Chat message {message.get_id()} created successfully.")
            return message.get_id()
        except Exception as e:
            logger.error(f"Error creating chat message {message.get_id()}: {e}")
            return None

    def update_chat_message(self, message: ChatMessageModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(message.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "sessionId": message.get_sessionId(),
                        "senderType": message.get_senderType(),
                        "intent": message.get_intent(),
                        "content": message.get_content(),
                        "citations": message.get_citations(),
                        "entities": message.get_entities(),
                        "createdAt": message.get_createdAt(),
                        "isActive": message.get_state(),
                    }
                )
                logger.info(f"Chat message {message.get_id()} updated successfully.")
                return True
            logger.warning(f"Chat message with ID {message.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating chat message {message.get_id()}: {e}")
            return False

    def delete_chat_message(self, message_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(message_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Chat message {message_id} deleted successfully.")
                return True
            logger.warning(f"Chat message with ID {message_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting chat message {message_id}: {e}")
            return False

    def block_chat_message(self, message_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(message_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Chat message {message_id} blocked successfully.")
                return True
            logger.warning(f"Chat message with ID {message_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking chat message {message_id}: {e}")
            return False

    def unblock_chat_message(self, message_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(message_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Chat message {message_id} unblocked successfully.")
                return True
            logger.warning(f"Chat message with ID {message_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking chat message {message_id}: {e}")
            return False