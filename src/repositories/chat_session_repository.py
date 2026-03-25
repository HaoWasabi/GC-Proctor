from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.chat_session_model import ChatSessionModel
from .base_repository import BaseRepository, logger


class ChatSessionRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "chat_sessions"

    def get_chat_session(self, session_id: str) -> Optional[ChatSessionModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(session_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return ChatSessionModel(**doc_snapshot.to_dict())
            logger.warning(f"Chat session with ID {session_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching chat session {session_id}: {e}")
            return None

    def get_all_chat_sessions(self) -> List[ChatSessionModel]:
        try:
            sessions: List[ChatSessionModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                sessions.append(ChatSessionModel(**doc.to_dict()))
            return sessions
        except Exception as e:
            logger.error(f"Error fetching all chat sessions: {e}")
            return []

    def create_chat_session(self, session: ChatSessionModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(session.get_id()).set(
                {
                    "id": session.get_id(),
                    "userId": session.get_userId(),
                    "channel": session.get_channel(),
                    "persona": session.get_persona(),
                    "sessionStatus": session.get_sessionStatus(),
                    "startedAt": session.get_startedAt(),
                    "endedAt": session.get_endedAt(),
                    "isActive": session.get_state(),
                }
            )
            logger.info(f"Chat session {session.get_id()} created successfully.")
            return session.get_id()
        except Exception as e:
            logger.error(f"Error creating chat session {session.get_id()}: {e}")
            return None

    def update_chat_session(self, session: ChatSessionModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(session.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "userId": session.get_userId(),
                        "channel": session.get_channel(),
                        "persona": session.get_persona(),
                        "sessionStatus": session.get_sessionStatus(),
                        "startedAt": session.get_startedAt(),
                        "endedAt": session.get_endedAt(),
                        "isActive": session.get_state(),
                    }
                )
                logger.info(f"Chat session {session.get_id()} updated successfully.")
                return True
            logger.warning(f"Chat session with ID {session.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating chat session {session.get_id()}: {e}")
            return False

    def delete_chat_session(self, session_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(session_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Chat session {session_id} deleted successfully.")
                return True
            logger.warning(f"Chat session with ID {session_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting chat session {session_id}: {e}")
            return False

    def block_chat_session(self, session_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(session_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Chat session {session_id} blocked successfully.")
                return True
            logger.warning(f"Chat session with ID {session_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking chat session {session_id}: {e}")
            return False

    def unblock_chat_session(self, session_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(session_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Chat session {session_id} unblocked successfully.")
                return True
            logger.warning(f"Chat session with ID {session_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking chat session {session_id}: {e}")
            return False
