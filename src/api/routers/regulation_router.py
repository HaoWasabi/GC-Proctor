from api.controllers.regulation_controller import RegulationController
from api.routers.router_factory import build_router


router = build_router(prefix="/regulations", tags=["Regulations"], controller=RegulationController())