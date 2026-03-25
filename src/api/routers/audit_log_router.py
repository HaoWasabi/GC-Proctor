from api.controllers.audit_log_controller import AuditLogController
from api.routers.router_factory import build_router


router = build_router(prefix="/audit-logs", tags=["Audit Logs"], controller=AuditLogController())