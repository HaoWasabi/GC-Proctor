from api.controllers.chat_session_controller import ChatSessionController
from api.routers.router_factory import build_router


router = build_router(prefix="/chat-sessions", tags=["Chat Sessions"], controller=ChatSessionController())