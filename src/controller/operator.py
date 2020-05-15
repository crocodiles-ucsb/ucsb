from typing import Optional

from pydantic import BaseModel
from src.controller.authorization_decorators import auth_required
from src.database.database import create_session
from src.database.models import Operator
from src.database.user_roles import UserRole
from src.templates import templates
from starlette.requests import Request


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
    @auth_required(UserRole.OPERATOR)
    async def get_operator_page(request: Request, operator_id: int):
        with create_session() as session:
            operator = session.query(Operator).filter(Operator.id == operator_id).one()
            return templates.TemplateResponse(
                'operator.html',
                {'request': request, 'operator': OperatorOut.from_orm(operator)},
            )
