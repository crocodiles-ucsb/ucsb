from abc import ABC

from src.DAL.tokens import check_auth
from src.DAL.utils import get_tokens
from src.database.user_roles import UserRole
from src.exceptions import AccessForbidden
from src.models import OutUser
from starlette.requests import Request


class AbstractUserController(ABC):
    @staticmethod
    async def check_auth(request: Request, user_type: UserRole) -> OutUser:
        user = await check_auth(get_tokens(request), True)
        if user.type != user_type.value:
            raise AccessForbidden()
        return user
