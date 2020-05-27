from typing import Optional

from pydantic import BaseModel
from src.controller.authorization_decorators import auth_required
from src.database.user_roles import UserRole
from src.templates import templates
from src.urls import Urls
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse


class OperatorOut(BaseModel):
    username: str
    first_name: str
    last_name: str
    patronymic: Optional[str]
    password_hash: str

    class Config:
        orm_mode = True


class OperatorsController:
    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_operator_page(request: Request):
        return RedirectResponse(f'{Urls.base_url.value}/contractors')

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_representative_add_form(
        req: Request, contractor_id: int
    ) -> _TemplateResponse:
        return templates.TemplateResponse(
            'operator-representative-add-form.html',
            {'request': req, 'contractor_id': contractor_id, 'base_url': Urls.base_url.value},
        )

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_contractor_add_form(req) -> _TemplateResponse:
        return templates.TemplateResponse(
            'operator-contractor-add-form.html',
            {'request': req, 'base_url': Urls.base_url.value},
        )
