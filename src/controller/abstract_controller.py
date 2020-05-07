from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Callable

from starlette.templating import Jinja2Templates

from src.config import service_settings
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.DAL.auth import check_authorization
from src.database.user_roles import UserRole
from src.exceptions import DALError, NeedRedirectToLogin, AccessForbidden
from src.models import OutUser
from src.templates import templates


class AbstractUserController(ABC):

    @staticmethod
    async def check_auth(request: Request, user_type: UserRole) -> OutUser:
        token = request.cookies.get('access_token')
        if token:
            user = await check_authorization(token)
            if user.type != user_type.value:
                raise AccessForbidden(request)
            return user
        raise NeedRedirectToLogin()


def error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NeedRedirectToLogin:
            return RedirectResponse(service_settings.login_url)
        except AccessForbidden as e:
            return templates.TemplateResponse('forbidden.html', {'request': e.request})

    return wrapper
