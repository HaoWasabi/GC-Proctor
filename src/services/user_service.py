from services.base_service import BaseService
from repositories.user_repository import UserRepository
from models.user_model import UserModel
from typing import Optional
from typing import List

class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()
        
    def get_user(self, user_id: str) -> Optional[UserModel]:
        return self.user_repository.get_user(user_id)
    
    def get_all_users(self) -> List[UserModel]:
        return self.user_repository.get_all_users()
    
    def create_user(self, user: UserModel) -> Optional[str]:
        return self.user_repository.create_user(user)
    
    def update_user(self, user: UserModel) -> bool:
        return self.user_repository.update_user(user)
    
    def delete_user(self, user_id: str) -> bool:
        return self.user_repository.delete_user(user_id)
    
    def block_user(self, user_id: str) -> bool:
        return self.user_repository.block_user(user_id)
    
    def unblock_user(self, user_id: str) -> bool:
        return self.user_repository.unblock_user(user_id)