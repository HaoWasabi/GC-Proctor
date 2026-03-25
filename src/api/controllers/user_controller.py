from api.controllers.base_entity_controller import BaseEntityController
from models.user_model import UserModel
from services.user_service import UserService


class UserController(BaseEntityController):
    def __init__(self):
        super().__init__(
            service=UserService(),
            model_cls=UserModel,
            entity_name="user",
            get_one_method="get_user",
            get_all_method="get_all_users",
            create_method="create_user",
            update_method="update_user",
            delete_method="delete_user",
            block_method="block_user",
            unblock_method="unblock_user",
        )