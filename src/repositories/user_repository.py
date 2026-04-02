from typing import List
from typing import Optional
from models.user_model import UserModel
from .base_repository import BaseRepository
from .base_repository import logger
from google.cloud.firestore_v1 import DocumentSnapshot

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.collection_name = "users"

    def _build_user_model(self, data: dict, fallback_id: str) -> UserModel:
        return UserModel(
            id=str(data.get("id") or data.get("_id") or fallback_id),
            userCode=str(data.get("userCode") or data.get("user_code") or ""),
            role=str(data.get("role") or ""),
            fullName=str(data.get("fullName") or data.get("full_name") or ""),
            email=str(data.get("email") or ""),
            authProvider=str(data.get("authProvider") or data.get("auth_provider") or "local"),
            password=str(data.get("password") or ""),
            createdAt=data.get("createdAt") or data.get("created_at") or "",
            updatedAt=data.get("updatedAt") or data.get("updated_at") or data.get("createdAt") or "",
            isActive=data.get("isActive", data.get("is_active", True)),
        )

    def _normalize_user_code(self, user_code: str) -> str:
        return str(user_code or "").strip().lower()

    def _matches_user_code(self, actual_user_code: str, expected_user_code: str) -> bool:
        return self._normalize_user_code(actual_user_code) == self._normalize_user_code(expected_user_code)
        
    def get_user(self, user_id: str) -> Optional[UserModel]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(user_id)
            doc_snapshot: DocumentSnapshot = doc_ref.get()
            if doc_snapshot.exists:
                data = doc_snapshot.to_dict()
                return self._build_user_model(data, doc_snapshot.id)
            else:
                logger.warning(f"User with ID {user_id} not found.")
                return None
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {e}")
            return None
        
    def get_user_by_userCode(self, user_code: str) -> Optional[UserModel]:
        try:
            normalized_user_code = self._normalize_user_code(user_code)
            query = self.db.collection(self.collection_name).where("userCode", "==", user_code).limit(1)
            docs = query.stream()
            for doc in docs:
                data = doc.to_dict()
                return self._build_user_model(data, doc.id)

            if normalized_user_code:
                for doc in self.db.collection(self.collection_name).stream():
                    data = doc.to_dict()
                    if self._matches_user_code(data.get("userCode") or data.get("user_code") or "", normalized_user_code):
                        return self._build_user_model(data, doc.id)

            logger.warning(f"User with userCode {user_code} not found.")
            return None
        except Exception as e:
            logger.error(f"Error fetching user by userCode {user_code}: {e}")
            return None
        
    def get_all_users(self) -> List[UserModel]:
        try:
            users = []
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                data = doc.to_dict()
                users.append(self._build_user_model(data, doc.id))
            return users
        except Exception as e:
            logger.error(f"Error fetching all users: {e}")
            return []
        
    def create_user(self, user: UserModel) -> Optional[str]:
        try:
            doc_ref = self.db.collection(self.collection_name).document(user.get_id())
            doc_ref.set({
                "id": user.get_id(),
                "userCode": user.get_userCode(),
                "role": user.get_role(),
                "fullName": user.get_fullName(),
                "email": user.get_email(),
                "authProvider": user.get_authProvider(),
                "password": user.get_password(),
                "createdAt": user.get_createdAt(),
                "updatedAt": user.get_updatedAt(),
                "isActive": user.get_state()
            })
            logger.info(f"User {user.get_id()} created successfully.")
            return user.get_id()
        except Exception as e:
            logger.error(f"Error creating user {user.get_id()}: {e}")
            return None
        
    def update_user(self, user: UserModel) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(user.get_id())
            if doc_ref.get().exists:
                doc_ref.update({
                    "userCode": user.get_userCode(),
                    "role": user.get_role(),
                    "fullName": user.get_fullName(),
                    "email": user.get_email(),
                    "authProvider": user.get_authProvider(),
                    "password": user.get_password(),
                    "createdAt": user.get_createdAt(),
                    "updatedAt": user.get_updatedAt(),
                    "isActive": user.get_state()
                })
                logger.info(f"User {user.get_id()} updated successfully.")
                return True
            else:
                logger.warning(f"User with ID {user.get_id()} not found for update.")
                return False
        except Exception as e:
            logger.error(f"Error updating user {user.get_id()}: {e}")
            return False
        
    def delete_user(self, user_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(user_id)
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f"User {user_id} deleted successfully.")
                return True
            else:
                logger.warning(f"User with ID {user_id} not found for deletion.")
                return False
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            return False
        
    def block_user(self, user_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(user_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": False})
                logger.info(f"User {user_id} blocked successfully.")
                return True
            else:
                logger.warning(f"User with ID {user_id} not found for blocking.")
                return False
        except Exception as e:
            logger.error(f"Error blocking user {user_id}: {e}")
            return False
        
    def unblock_user(self, user_id: str) -> bool:
        try:
            doc_ref = self.db.collection(self.collection_name).document(user_id)
            if doc_ref.get().exists:
                doc_ref.update({"isActive": True})
                logger.info(f"User {user_id} unblocked successfully.")
                return True
            else:
                logger.warning(f"User with ID {user_id} not found for unblocking.")
                return False
        except Exception as e:
            logger.error(f"Error unblocking user {user_id}: {e}")
            return False