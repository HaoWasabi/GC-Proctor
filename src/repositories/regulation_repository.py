from typing import List, Optional
from google.cloud.firestore_v1 import DocumentSnapshot
from models.regulation_model import RegulationModel
from .base_repository import BaseRepository, logger


class RegulationRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "regulations"

    def get_regulation(self, regulation_id: str) -> Optional[RegulationModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(regulation_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                return RegulationModel(**doc_snapshot.to_dict())
            logger.warning(f"Regulation with ID {regulation_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching regulation {regulation_id}: {e}")
            return None

    def get_all_regulations(self) -> List[RegulationModel]:
        try:
            regulations: List[RegulationModel] = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                regulations.append(RegulationModel(**doc.to_dict()))
            return regulations
        except Exception as e:
            logger.error(f"Error fetching all regulations: {e}")
            return []

    def create_regulation(self, regulation: RegulationModel) -> Optional[str]:
        try:
            self.db.collection(self.collection_name).document(regulation.get_id()).set(
                {
                    "id": regulation.get_id(),
                    "regulationCode": regulation.get_regulationCode(),
                    "title": regulation.get_title(),
                    "version": regulation.get_version(),
                    "effectiveDate": regulation.get_effectiveDate(),
                    "sourceUrl": regulation.get_sourceUrl(),
                    "updatedAt": regulation.get_updatedAt(),
                    "isActive": regulation.get_state(),
                }
            )
            logger.info(f"Regulation {regulation.get_id()} created successfully.")
            return regulation.get_id()
        except Exception as e:
            logger.error(f"Error creating regulation {regulation.get_id()}: {e}")
            return None

    def update_regulation(self, regulation: RegulationModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(regulation.get_id())
            if doc_ref.get().exists:
                doc_ref.update(
                    {
                        "regulationCode": regulation.get_regulationCode(),
                        "title": regulation.get_title(),
                        "version": regulation.get_version(),
                        "effectiveDate": regulation.get_effectiveDate(),
                        "sourceUrl": regulation.get_sourceUrl(),
                        "updatedAt": regulation.get_updatedAt(),
                        "isActive": regulation.get_state(),
                    }
                )
                logger.info(f"Regulation {regulation.get_id()} updated successfully.")
                return True
            logger.warning(f"Regulation with ID {regulation.get_id()} not found for update.")
            return False
        except Exception as e:
            logger.error(f"Error updating regulation {regulation.get_id()}: {e}")
            return False

    def delete_regulation(self, regulation_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(regulation_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"Regulation {regulation_id} deleted successfully.")
                return True
            logger.warning(f"Regulation with ID {regulation_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting regulation {regulation_id}: {e}")
            return False

    def block_regulation(self, regulation_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(regulation_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"Regulation {regulation_id} blocked successfully.")
                return True
            logger.warning(f"Regulation with ID {regulation_id} not found for blocking.")
            return False
        except Exception as e:
            logger.error(f"Error blocking regulation {regulation_id}: {e}")
            return False

    def unblock_regulation(self, regulation_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(regulation_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"Regulation {regulation_id} unblocked successfully.")
                return True
            logger.warning(f"Regulation with ID {regulation_id} not found for unblocking.")
            return False
        except Exception as e:
            logger.error(f"Error unblocking regulation {regulation_id}: {e}")
            return False
