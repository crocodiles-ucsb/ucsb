from typing import Optional

from pydantic import BaseModel
from src.controller.authorization_decorators import auth_required
from src.database.user_roles import UserRole
from src.templates import templates
from starlette.requests import Request
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
        return templates.TemplateResponse('operator.html', {'request': request})

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_representative_add_form(req: Request) -> _TemplateResponse:
        return templates.TemplateResponse(
            'operator-representative-add-form.html', {'request': req}
        )
