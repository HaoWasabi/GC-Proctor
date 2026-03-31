from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.feedback_model import FeedbackModel
from .base_repository import BaseRepository, logger


class FeedbackRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "feedbacks"

    def get_feedback(self, feedback_id: str) -> Optional[FeedbackModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(feedback_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return FeedbackModel(**doc_snapshot.to_dict())
            logger.warning(f"Feedback with ID {feedback_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching feedback {feedback_id}: {e}")
            return None

    def get_all_feedbacks(self) -> List[FeedbackModel]:
        try:
            feedbacks: List[FeedbackModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                feedbacks.append(FeedbackModel(**doc.to_dict()))
            return feedbacks
        except Exception as e:
            logger.error(f"Error fetching all feedbacks: {e}")
            return []

    def create_feedback(self, feedback: FeedbackModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(feedback.get_id()).set(
                {
                    "id": feedback.get_id(),
                    "userId": feedback.get_userId(),
                    "messageId": feedback.get_messageId(),
                    "rating": feedback.get_rating(),
                    "comment": feedback.get_comment(),
                    "createdAt": feedback.get_createdAt(),
                    "isActive": feedback.get_state(),
                }
            )
            logger.info(f"Feedback {feedback.get_id()} created successfully.")
            return feedback.get_id()
        except Exception as e:
            logger.error(f"Error creating feedback {feedback.get_id()}: {e}")
            return None

    def update_feedback(self, feedback: FeedbackModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(feedback.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "userId": feedback.get_userId(),
                        "messageId": feedback.get_messageId(),
                        "rating": feedback.get_rating(),
                        "comment": feedback.get_comment(),
                        "createdAt": feedback.get_createdAt(),
                        "isActive": feedback.get_state(),
                    }
                )
                logger.info(f"Feedback {feedback.get_id()} updated successfully.")
                return True
            logger.warning(f"Feedback with ID {feedback.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating feedback {feedback.get_id()}: {e}")
            return False

    def delete_feedback(self, feedback_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(feedback_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Feedback {feedback_id} deleted successfully.")
                return True
            logger.warning(f"Feedback with ID {feedback_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting feedback {feedback_id}: {e}")
            return False

    def block_feedback(self, feedback_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(feedback_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Feedback {feedback_id} blocked successfully.")
                return True
            logger.warning(f"Feedback with ID {feedback_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking feedback {feedback_id}: {e}")
            return False

    def unblock_feedback(self, feedback_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(feedback_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Feedback {feedback_id} unblocked successfully.")
                return True
            logger.warning(f"Feedback with ID {feedback_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking feedback {feedback_id}: {e}")
            return False

    def get_feedback_by_message(self, message_id: str) -> List[FeedbackModel]:
            try:
                feedbacks = []
                docs = self.db.collection(self.collection_name).where("messageId", "==", message_id).stream()
                for doc in docs:
                    feedbacks.append(FeedbackModel(**doc.to_dict()))
                return feedbacks
            except Exception as e:
                logger.error(f"Error fetching feedback for message {message_id}: {e}")
                return []
