from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.audit_log_model import AuditLogModel
from .base_repository import BaseRepository, logger


class AuditLogRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "audit_logs"

    def get_audit_log(self, audit_log_id: str) -> Optional[AuditLogModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(audit_log_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return AuditLogModel(**doc_snapshot.to_dict())
            logger.warning(f"Audit log with ID {audit_log_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching audit log {audit_log_id}: {e}")
            return None

    def get_all_audit_logs(self) -> List[AuditLogModel]:
        try:
            audit_logs: List[AuditLogModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                audit_logs.append(AuditLogModel(**doc.to_dict()))
            return audit_logs
        except Exception as e:
            logger.error(f"Error fetching all audit logs: {e}")
            return []

    def create_audit_log(self, audit_log: AuditLogModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(audit_log.get_id()).set(
                {
                    "id": audit_log.get_id(),
                    "actorUserId": audit_log.get_actorUserId(),
                    "actionType": audit_log.get_actionType(),
                    "targetCollection": audit_log.get_targetCollection(),
                    "targetId": audit_log.get_targetId(),
                    "metadata": audit_log.get_metadata(),
                    "createdAt": audit_log.get_createdAt(),
                    "isActive": audit_log.get_state(),
                }
            )
            logger.info(f"Audit log {audit_log.get_id()} created successfully.")
            return audit_log.get_id()
        except Exception as e:
            logger.error(f"Error creating audit log {audit_log.get_id()}: {e}")
            return None

    def update_audit_log(self, audit_log: AuditLogModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(audit_log.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "actorUserId": audit_log.get_actorUserId(),
                        "actionType": audit_log.get_actionType(),
                        "targetCollection": audit_log.get_targetCollection(),
                        "targetId": audit_log.get_targetId(),
                        "metadata": audit_log.get_metadata(),
                        "createdAt": audit_log.get_createdAt(),
                        "isActive": audit_log.get_state(),
                    }
                )
                logger.info(f"Audit log {audit_log.get_id()} updated successfully.")
                return True
            logger.warning(f"Audit log with ID {audit_log.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating audit log {audit_log.get_id()}: {e}")
            return False

    def delete_audit_log(self, audit_log_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(audit_log_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Audit log {audit_log_id} deleted successfully.")
                return True
            logger.warning(f"Audit log with ID {audit_log_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting audit log {audit_log_id}: {e}")
            return False

    def block_audit_log(self, audit_log_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(audit_log_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Audit log {audit_log_id} blocked successfully.")
                return True
            logger.warning(f"Audit log with ID {audit_log_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking audit log {audit_log_id}: {e}")
            return False

    def unblock_audit_log(self, audit_log_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(audit_log_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Audit log {audit_log_id} unblocked successfully.")
                return True
            logger.warning(f"Audit log with ID {audit_log_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking audit log {audit_log_id}: {e}")
            return False
