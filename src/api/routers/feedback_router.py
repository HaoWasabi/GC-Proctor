from api.controllers.feedback_controller import FeedbackController
from api.routers.router_factory import build_router


router = build_router(prefix="/feedbacks", tags=["Feedbacks"], controller=FeedbackController())