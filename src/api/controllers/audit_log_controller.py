from api.controllers.base_entity_controller import BaseEntityController
from models.audit_log_model import AuditLogModel
from services.audit_log_service import AuditLogService


class AuditLogController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=AuditLogService(),
            model_cls=AuditLogModel,
            entity_name="audit_log",
            get_one_method="get_audit_log",
            get_all_method="get_all_audit_logs",
            create_method="create_audit_log",
            update_method="update_audit_log",
            delete_method="delete_audit_log",
            block_method="block_audit_log",
            unblock_method="unblock_audit_log",
        )