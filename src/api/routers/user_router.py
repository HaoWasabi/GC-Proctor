from api.controllers.user_controller import UserController
from api.routers.router_factory import build_router


router = build_router(prefix="/users", tags=["Users"], controller=UserController())