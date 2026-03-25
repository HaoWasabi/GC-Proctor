from typing import List
from typing import Optional

from models.audit_log_model import AuditLogModel
from repositories.audit_log_repository import AuditLogRepository
from services.base_service import BaseService


class AuditLogService(BaseService):
    def __init__(self):
        super().__init__()
        self.audit_log_repository = AuditLogRepository()

    def get_audit_log(self, audit_log_id: str) -> Optional[AuditLogModel]:
        return self.audit_log_repository.get_audit_log(audit_log_id)

    def get_all_audit_logs(self) -> List[AuditLogModel]:
        return self.audit_log_repository.get_all_audit_logs()

    def create_audit_log(self, audit_log: AuditLogModel) -> Optional[str]:
        return self.audit_log_repository.create_audit_log(audit_log)

    def update_audit_log(self, audit_log: AuditLogModel) -> bool:
        return self.audit_log_repository.update_audit_log(audit_log)

    def delete_audit_log(self, audit_log_id: str) -> bool:
        return self.audit_log_repository.delete_audit_log(audit_log_id)

    def block_audit_log(self, audit_log_id: str) -> bool:
        return self.audit_log_repository.block_audit_log(audit_log_id)

    def unblock_audit_log(self, audit_log_id: str) -> bool:
        return self.audit_log_repository.unblock_audit_log(audit_log_id)