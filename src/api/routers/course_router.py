from api.controllers.course_controller import CourseController
from api.routers.router_factory import build_router


router = build_router(prefix="/courses", tags=["Courses"], controller=CourseController())