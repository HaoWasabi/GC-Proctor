from api.controllers.exam_controller import ExamController
from api.routers.router_factory import build_router


router = build_router(prefix="/exams", tags=["Exams"], controller=ExamController())