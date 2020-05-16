from starlette.responses import RedirectResponse

from src.controller.authorization_decorators import auth_required
from src.DAL.registration import SimpleRegistrationParams
from src.DAL.users.admin import Admin
from src.DAL.users.operator import Operator, OperatorAddingParams, OperatorToAddingOut
from src.DAL.users.security import Security, SecurityAddingParams
from src.database.user_roles import UserRole
from src.models import OperatorIn, OutUser, SecurityIn
from src.templates import templates
from src.urls import Urls
from starlette.requests import Request
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
        return templates.TemplateResponse(
            'add_operator_form.html', {'request': req, 'base_url': Urls.base_url.value},
        )

    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def add_security_form(req: Request, admin_id: int) -> _TemplateResponse:
        return templates.TemplateResponse(
            'add_security_form.html',
            {'request': req, 'base_url': Urls.base_url.value, 'admin_id': admin_id},
        )

    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def get_admin_page(req: Request, admin_id: int) -> RedirectResponse:
        return RedirectResponse(f"{Urls.base_url.value}/admins/{admin_id}/operators")

    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def get_operators(
            req: Request, admin_id: int, page: int, pending: bool
    ) -> _TemplateResponse:
        if pending:
            return await AdminsController.get_operators_pending_register(req, admin_id, page)
        operators = await Admin().get_operators(page)
        return templates.TemplateResponse(
            'admin-operators.html',
            {'request': req, 'admin_id': admin_id, 'base_url': Urls.base_url.value, 'operators': operators}
        )

    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def get_operators_pending_register(
            req: Request, admin_id: int, page: int
    ) -> _TemplateResponse:
        # operators = await Admin().get_operators(page)
        return templates.TemplateResponse(
            'admin-operators-waiting.html',
            {'request': req, 'admin_id': admin_id, 'base_url': Urls.base_url.value}
        )

    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def get_securities_page(req: Request, admin_id: int, page: int, pending: bool) -> _TemplateResponse:
        if pending:
            return await AdminsController.get_securities_pending_register(req, admin_id, page)
        securities = await Admin().get_securities(page)
        return templates.TemplateResponse(
            'admin-securities.html',
            {'request': req, 'admin_id': admin_id, 'base_url': Urls.base_url.value, "securities": securities},
        )

    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def get_securities_pending_register(
            req: Request, admin_id: int, page: int
    ) -> _TemplateResponse:
        # operators = await Admin().get_operators(page)
        return templates.TemplateResponse(
            'admin-securities-waiting.html',
            {'request': req, 'admin_id': admin_id, 'base_url': Urls.base_url.value}
        )

    @staticmethod
    @auth_required(UserRole.ADMIN, check_id=False, auth_redirect=False)
    async def add_security(req: Request, security_in: SecurityIn):
        return await Security().add_user(
            SecurityAddingParams(
                first_name=security_in.first_name,
                last_name=security_in.last_name,
                patronymic=security_in.patronymic,
                position=security_in.position,
            )
        )

    @staticmethod
    @auth_required(UserRole.ADMIN, check_id=False, auth_redirect=False)
    async def add_operator(
            req: Request, operator_in: OperatorIn
    ) -> OperatorToAddingOut:
        return await Operator().add_user(
            OperatorAddingParams(
                first_name=operator_in.first_name,
                last_name=operator_in.last_name,
                patronymic=operator_in.patronymic,
            )
        )
