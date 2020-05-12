from http import HTTPStatus

from src.config import service_settings
from src.controller.authorization_decorators import auth_required
from src.DAL.registration import SimpleRegistrationParams
from src.DAL.users.admin import Admin
from src.DAL.users.operator import Operator
from src.database.user_roles import UserRole
from src.models import OperatorAddingParams, OutUser, OperatorToRegisterOut, OperatorIn
from src.templates import templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse


class AdminsController:
    @staticmethod
    async def add(username: str, password: str) -> OutUser:
        return await Admin().register_user(
            SimpleRegistrationParams(username, password, UserRole.ADMIN)
        )

    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def add_operator_form(req: Request, admin_id: int) -> _TemplateResponse:
        return templates.TemplateResponse('add_operator_form.html', {'request': req, 'base_url':service_settings.base_url})

    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def get_admin_page(req: Request, admin_id: int) -> _TemplateResponse:
        return templates.TemplateResponse(
            'admin.html', {'request': req, 'admin_id': admin_id, 'base_url':service_settings.base_url}
        )

    @staticmethod
    @auth_required(UserRole.ADMIN, check_id=False, auth_redirect=False)
    async def add_operator(
            req: Request,
            operator_in: OperatorIn
    ) -> OperatorToRegisterOut:
        return await Operator().add_user(
            OperatorAddingParams(
                first_name=operator_in.first_name, last_name=operator_in.last_name, patronymic=operator_in.patronymic
            )
        )
