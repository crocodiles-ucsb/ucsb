from src.controller.abstract_controller import AbstractUserController
from src.DAL.admin import Admin
from src.DAL.registration import SimpleRegistrationParams
from src.DAL.utils import auth_handler
from src.database.user_roles import UserRole
from src.models import OutUser
from src.templates import templates
from starlette.requests import Request
from starlette.templating import _TemplateResponse


class AdminsController(AbstractUserController):
    @staticmethod
    async def add(username: str, password: str) -> OutUser:
        return await Admin().register_user(
            SimpleRegistrationParams(username, password, UserRole.ADMIN)
        )

    @staticmethod
    @auth_handler
    async def get_admin_page(admin_id: int, req: Request) -> _TemplateResponse:
        user = await AdminsController.check_auth(req, UserRole.ADMIN)
        return templates.TemplateResponse('admin.html', {'request': req, 'user': user})
