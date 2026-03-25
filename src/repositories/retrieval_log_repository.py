from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.retrieval_log_model import RetrievalLogModel
from .base_repository import BaseRepository, logger


class RetrievalLogRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "retrieval_logs"

    def get_retrieval_log(self, retrieval_log_id: str) -> Optional[RetrievalLogModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(retrieval_log_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return RetrievalLogModel(**doc_snapshot.to_dict())
            logger.warning(f"Retrieval log with ID {retrieval_log_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching retrieval log {retrieval_log_id}: {e}")
            return None

    def get_all_retrieval_logs(self) -> List[RetrievalLogModel]:
        try:
            retrieval_logs: List[RetrievalLogModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                retrieval_logs.append(RetrievalLogModel(**doc.to_dict()))
            return retrieval_logs
        except Exception as e:
            logger.error(f"Error fetching all retrieval logs: {e}")
            return []

    def create_retrieval_log(self, retrieval_log: RetrievalLogModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(retrieval_log.get_id()).set(
                {
                    "id": retrieval_log.get_id(),
                    "messageId": retrieval_log.get_messageId(),
                    "chunkId": retrieval_log.get_chunkId(),
                    "similarity": retrieval_log.get_similarity(),
                    "retrieverVersion": retrieval_log.get_retrieverVersion(),
                    "createdAt": retrieval_log.get_createdAt(),
                    "isActive": retrieval_log.get_state(),
                }
            )
            logger.info(f"Retrieval log {retrieval_log.get_id()} created successfully.")
            return retrieval_log.get_id()
        except Exception as e:
            logger.error(f"Error creating retrieval log {retrieval_log.get_id()}: {e}")
            return None

    def update_retrieval_log(self, retrieval_log: RetrievalLogModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(retrieval_log.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "messageId": retrieval_log.get_messageId(),
                        "chunkId": retrieval_log.get_chunkId(),
                        "similarity": retrieval_log.get_similarity(),
                        "retrieverVersion": retrieval_log.get_retrieverVersion(),
                        "createdAt": retrieval_log.get_createdAt(),
                        "isActive": retrieval_log.get_state(),
                    }
                )
                logger.info(f"Retrieval log {retrieval_log.get_id()} updated successfully.")
                return True
            logger.warning(f"Retrieval log with ID {retrieval_log.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating retrieval log {retrieval_log.get_id()}: {e}")
            return False

    def delete_retrieval_log(self, retrieval_log_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(retrieval_log_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Retrieval log {retrieval_log_id} deleted successfully.")
                return True
            logger.warning(f"Retrieval log with ID {retrieval_log_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting retrieval log {retrieval_log_id}: {e}")
            return False

    def block_retrieval_log(self, retrieval_log_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(retrieval_log_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Retrieval log {retrieval_log_id} blocked successfully.")
                return True
            logger.warning(f"Retrieval log with ID {retrieval_log_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking retrieval log {retrieval_log_id}: {e}")
            return False

    def unblock_retrieval_log(self, retrieval_log_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(retrieval_log_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Retrieval log {retrieval_log_id} unblocked successfully.")
                return True
            logger.warning(f"Retrieval log with ID {retrieval_log_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking retrieval log {retrieval_log_id}: {e}")
            return False
