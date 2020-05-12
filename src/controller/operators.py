from src.controller.authorization_decorators import auth_required
from src.database.user_roles import UserRole
from starlette.requests import Request


class OperatorsController:
    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def add_operator(req: Request):
        pass

    @staticmethod
    @auth_required(UserRole.ADMIN)
    async def get_operators():
        pass
