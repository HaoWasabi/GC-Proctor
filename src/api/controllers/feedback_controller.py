from api.controllers.base_entity_controller import BaseEntityController
from models.feedback_model import FeedbackModel
from services.feedback_service import FeedbackService


class FeedbackController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=FeedbackService(),
            model_cls=FeedbackModel,
            entity_name="feedback",
            get_one_method="get_feedback",
            get_all_method="get_all_feedbacks",
            create_method="create_feedback",
            update_method="update_feedback",
            delete_method="delete_feedback",
            block_method="block_feedback",
            unblock_method="unblock_feedback",
            get_feedback_by_message_id_method="get_feedback_by_message_id",
            submit_feedback_method="submit_feedback",
        )