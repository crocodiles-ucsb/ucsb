from http import HTTPStatus
from typing import cast


from src.DAL.tokens import check_auth, get_tokens
from src.DAL.utils import get_url_postfix
from src.database.user_roles import UserRole
from src.exceptions import (
    AccessForbidden,
    AuthDataOutdated,
    NeedRedirectToLogin,
    NeedRedirectToRefreshToken,
    RedirectToUser,
)
from src.models import OutUser
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from src.urls import Urls


def auth_required(
    user_role: UserRole, check_id: bool = True, auth_redirect: bool = True
):
    def decorator(func):
        @auth_handler
        async def wrapper(req: Request, *args, **kwargs):
            user = await check_auth(get_tokens(req), True, auth_redirect=auth_redirect)
            user = cast(OutUser, user)
            if user.type != user_role.value:
                raise AccessForbidden()
            if check_id:
                user_id = args[0]
                if user.id != user_id:
                    raise AccessForbidden()
                return await func(req, *args, **kwargs)
            return await func(req, *args, **kwargs)

        return wrapper

    return decorator


def auth_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AccessForbidden:
            return (
                RedirectResponse(Urls.forbidden_url.value),
                HTTPStatus.SEE_OTHER.value,
            )
        except RedirectToUser as e:
            return RedirectResponse(
                f'{Urls.base_url.value}{get_url_postfix(e.user)}',
                HTTPStatus.SEE_OTHER.value,
            )
        except NeedRedirectToLogin:
            return RedirectResponse(
                Urls.login_url.value, HTTPStatus.SEE_OTHER.value
            )
        except NeedRedirectToRefreshToken as e:
            return RedirectResponse(
                f'{Urls.refresh_token_url.value}?access_token={e.tokens.access_token.decode()}&refresh_token'
                f'={e.tokens.refresh_token.decode()}',
                HTTPStatus.FOUND.value,
            )
        except AuthDataOutdated:
            return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED.value)

    return wrapper
