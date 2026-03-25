from api.controllers.base_entity_controller import BaseEntityController
from models.chat_message_model import ChatMessageModel
from services.chat_message_service import ChatMessageService


class ChatMessageController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=ChatMessageService(),
            model_cls=ChatMessageModel,
            entity_name="chat_message",
            get_one_method="get_chat_message",
            get_all_method="get_all_chat_messages",
            create_method="create_chat_message",
            update_method="update_chat_message",
            delete_method="delete_chat_message",
            block_method="block_chat_message",
            unblock_method="unblock_chat_message",
        )