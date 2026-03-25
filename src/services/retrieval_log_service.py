from typing import List
from typing import Optional

from models.retrieval_log_model import RetrievalLogModel
from repositories.retrieval_log_repository import RetrievalLogRepository
from services.base_service import BaseService


class RetrievalLogService(BaseService):
    def __init__(self):
        super().__init__()
        self.retrieval_log_repository = RetrievalLogRepository()

    def get_retrieval_log(self, retrieval_log_id: str) -> Optional[RetrievalLogModel]:
        return self.retrieval_log_repository.get_retrieval_log(retrieval_log_id)

    def get_all_retrieval_logs(self) -> List[RetrievalLogModel]:
        return self.retrieval_log_repository.get_all_retrieval_logs()

    def create_retrieval_log(self, retrieval_log: RetrievalLogModel) -> Optional[str]:
        return self.retrieval_log_repository.create_retrieval_log(retrieval_log)

    def update_retrieval_log(self, retrieval_log: RetrievalLogModel) -> bool:
        return self.retrieval_log_repository.update_retrieval_log(retrieval_log)

    def delete_retrieval_log(self, retrieval_log_id: str) -> bool:
        return self.retrieval_log_repository.delete_retrieval_log(retrieval_log_id)

    def block_retrieval_log(self, retrieval_log_id: str) -> bool:
        return self.retrieval_log_repository.block_retrieval_log(retrieval_log_id)

    def unblock_retrieval_log(self, retrieval_log_id: str) -> bool:
        return self.retrieval_log_repository.unblock_retrieval_log(retrieval_log_id)