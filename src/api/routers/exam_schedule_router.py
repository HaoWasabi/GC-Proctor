from api.controllers.exam_schedule_controller import ExamScheduleController
from api.routers.router_factory import build_router


router = build_router(prefix="/exam-schedules", tags=["Exam Schedules"], controller=ExamScheduleController())