from typing import List
from typing import Optional

from models.regulation_model import RegulationModel
from repositories.regulation_repository import RegulationRepository
from services.base_service import BaseService


class RegulationService(BaseService):
    def __init__(self):
        super().__init__()
        self.regulation_repository = RegulationRepository()

    def get_regulation(self, regulation_id: str) -> Optional[RegulationModel]:
        return self.regulation_repository.get_regulation(regulation_id)

    def get_all_regulations(self) -> List[RegulationModel]:
        return self.regulation_repository.get_all_regulations()

    def create_regulation(self, regulation: RegulationModel) -> Optional[str]:
        return self.regulation_repository.create_regulation(regulation)

    def update_regulation(self, regulation: RegulationModel) -> bool:
        return self.regulation_repository.update_regulation(regulation)

    def delete_regulation(self, regulation_id: str) -> bool:
        return self.regulation_repository.delete_regulation(regulation_id)

    def block_regulation(self, regulation_id: str) -> bool:
        return self.regulation_repository.block_regulation(regulation_id)

    def unblock_regulation(self, regulation_id: str) -> bool:
        return self.regulation_repository.unblock_regulation(regulation_id)