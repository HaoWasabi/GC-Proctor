from api.controllers.chat_message_controller import ChatMessageController
from api.routers.router_factory import build_router


router = build_router(prefix="/chat-messages", tags=["Chat Messages"], controller=ChatMessageController())