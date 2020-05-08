from dataclasses import dataclass
from io import StringIO
from typing import Optional

from src.config import service_settings
from src.database.user_roles import UserRole
from src.exceptions import (
    AccessForbidden,
    NeedRedirectToLogin,
    NeedRedirectToRefreshToken,
    RedirectToUser,
)
from src.models import OutUser
from starlette.requests import Request
from starlette.responses import RedirectResponse


def get_url_postfix(user: OutUser) -> str:
    res = StringIO()
    res.write('/')
    if user.type == UserRole.SECURITY.value:
        res.write(user.type[:-1])
        res.write('ies')
    else:
        res.write(user.type)
        res.write('s')
    res.write('/')
    res.write(str(user.id))
    return res.getvalue()


def auth_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NeedRedirectToLogin:
            return RedirectResponse(service_settings.login_url)
        except AccessForbidden:
            return RedirectResponse(service_settings.forbidden_url)
        except RedirectToUser as e:
            return RedirectResponse(
                f'{service_settings.base_url}{get_url_postfix(e.user)}'
            )
        except NeedRedirectToRefreshToken as e:
            return RedirectResponse(
                f'{service_settings.refresh_token_url}?access_token={e.tokens.access_token.decode()}&refresh_token'
                f'={e.tokens.refresh_token.decode()}'
            )

    return wrapper


@dataclass
class Tokens:
    access_token: Optional[str]
    refresh_token: Optional[str]


def get_tokens(req: Request) -> Tokens:
    cookies = req.cookies
    return Tokens(cookies.get('access_token'), cookies.get('refresh_token'))
