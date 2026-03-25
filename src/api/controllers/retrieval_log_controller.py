from api.controllers.base_entity_controller import BaseEntityController
from models.retrieval_log_model import RetrievalLogModel
from services.retrieval_log_service import RetrievalLogService


class RetrievalLogController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=RetrievalLogService(),
            model_cls=RetrievalLogModel,
            entity_name="retrieval_log",
            get_one_method="get_retrieval_log",
            get_all_method="get_all_retrieval_logs",
            create_method="create_retrieval_log",
            update_method="update_retrieval_log",
            delete_method="delete_retrieval_log",
            block_method="block_retrieval_log",
            unblock_method="unblock_retrieval_log",
        )