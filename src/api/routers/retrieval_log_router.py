from api.controllers.retrieval_log_controller import RetrievalLogController
from api.routers.router_factory import build_router


router = build_router(prefix="/retrieval-logs", tags=["Retrieval Logs"], controller=RetrievalLogController())