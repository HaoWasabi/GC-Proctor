from api.controllers.base_entity_controller import BaseEntityController
from models.regulation_model import RegulationModel
from services.regulation_service import RegulationService


class RegulationController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=RegulationService(),
            model_cls=RegulationModel,
            entity_name="regulation",
            get_one_method="get_regulation",
            get_all_method="get_all_regulations",
            create_method="create_regulation",
            update_method="update_regulation",
            delete_method="delete_regulation",
            block_method="block_regulation",
            unblock_method="unblock_regulation",
        )