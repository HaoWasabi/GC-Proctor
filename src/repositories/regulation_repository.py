import openpyxl
from datetime import datetime
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

    def import_from_excel_batch(self, file_path: str):
        try:
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active  # Hoặc wb["Tên_Sheet"]
            
            batch = self.get_batch()
            count = 0

            # Giả sử: A: ID, B: Code, C: Title, D: Version, E: Date, F: URL
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row[1]: continue # Bỏ qua dòng trống
                
                reg_id = str(row[0]) if row[0] else None
                new_reg = RegulationModel(
                    id=reg_id,
                    regulationCode=str(row[1]),
                    title=str(row[2]),
                    version=str(row[3]),
                    effectiveDate=str(row[4] if isinstance(row[4], datetime) else datetime.now()),
                    sourceUrl=str(row[5]),
                    updatedAt=str(datetime.now())
                )
                
                # Tạo document reference
                doc_ref = self.db.collection(self.collection_name).document(reg_id or new_reg.get_regulationCode())
                batch.set(doc_ref, {
                    "regulationCode": new_reg.get_regulationCode(),
                    "title": new_reg.get_title(),
                    "version": new_reg.get_version(),
                    "effectiveDate": new_reg.get_effectiveDate(),
                    "sourceUrl": new_reg.get_sourceUrl(),
                    "updatedAt": new_reg.get_updatedAt(),
                    "isActive": True
                })
                
                count += 1
                if count % 500 == 0: # Firestore giới hạn 500 thao tác mỗi batch
                    batch.commit()
                    batch = self.get_batch()

            batch.commit()
            return {"success": 1, "failed": 0, "errors": []}
        except Exception as e:
            logger.error(f"Error importing regulations from Excel: {e}")
            return {"success": 0, "failed": 0, "errors": [str(e)]}