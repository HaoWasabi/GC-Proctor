from typing import List
from typing import Optional

from models.feedback_model import FeedbackModel
from repositories.feedback_repository import FeedbackRepository
from services.base_service import BaseService


class FeedbackService(BaseService):
    def __init__(self):
        super().__init__()
        self.feedback_repository = FeedbackRepository()

    def get_feedback(self, feedback_id: str) -> Optional[FeedbackModel]:
        return self.feedback_repository.get_feedback(feedback_id)

    def get_all_feedbacks(self) -> List[FeedbackModel]:
        return self.feedback_repository.get_all_feedbacks()

    def create_feedback(self, feedback: FeedbackModel) -> Optional[str]:
        return self.feedback_repository.create_feedback(feedback)

    def update_feedback(self, feedback: FeedbackModel) -> bool:
        return self.feedback_repository.update_feedback(feedback)

    def delete_feedback(self, feedback_id: str) -> bool:
        return self.feedback_repository.delete_feedback(feedback_id)

    def block_feedback(self, feedback_id: str) -> bool:
        return self.feedback_repository.block_feedback(feedback_id)

    def unblock_feedback(self, feedback_id: str) -> bool:
        return self.feedback_repository.unblock_feedback(feedback_id)
    
    def get_feedback_by_message_id(self, message_id: str) -> Optional[FeedbackModel]:
        return self.feedback_repository.get_feedback_by_message_id(message_id)
    
    def submit_feedback(self, feedback: FeedbackModel) -> Optional[str]:
        # Bạn có thể thêm logic kiểm tra rating ở đây (ví dụ: 1-5)
        if not (1 <= feedback.get_rating() <= 5):
            return None
        return self.feedback_repository.create_feedback(feedback)