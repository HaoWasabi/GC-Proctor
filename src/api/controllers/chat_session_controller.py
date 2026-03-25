from api.controllers.base_entity_controller import BaseEntityController
from models.chat_session_model import ChatSessionModel
from services.chat_session_service import ChatSessionService


class ChatSessionController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=ChatSessionService(),
            model_cls=ChatSessionModel,
            entity_name="chat_session",
            get_one_method="get_chat_session",
            get_all_method="get_all_chat_sessions",
            create_method="create_chat_session",
            update_method="update_chat_session",
            delete_method="delete_chat_session",
            block_method="block_chat_session",
            unblock_method="unblock_chat_session",
        )