from starlette.requests import Request

from src.DAL.admin import Admin
from src.DAL.registration import SimpleRegistrationParams
from src.controller.abstract_controller import AbstractUserController, error_handler
from src.database.user_roles import UserRole
from src.models import OutUser


class AdminsController(AbstractUserController):

    @staticmethod
    async def add(username: str, password: str) -> OutUser:
        return await Admin().register_user(
            SimpleRegistrationParams(username, password, UserRole.ADMIN)
        )

    @staticmethod
    @error_handler
    async def get_admin_page(admin_id: int, req: Request):
        user = await AbstractUserController.check_auth(req, UserRole.ADMIN)
        return user.username
