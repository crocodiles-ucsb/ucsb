from dataclasses import dataclass
from http import HTTPStatus
from typing import Awaitable, Optional, cast

from src.DAL import auth
from src.DAL.auth import check_authorization
from src.database.database import create_session, run_in_threadpool
from src.database.models import User
from src.exceptions import (
    AccessTokenOutdatedError,
    AuthDataOutdated,
    DALError,
    NeedRedirectToLogin,
    NeedRedirectToRefreshToken,
    RedirectToUser,
)
from src.models import OutUser
from starlette.requests import Request


@dataclass
class Tokens:
    access_token: Optional[str]
    refresh_token: Optional[str]


def get_tokens(req: Request) -> Tokens:
    cookies = req.cookies
    return Tokens(cookies.get('access_token'), cookies.get('refresh_token'))


@run_in_threadpool
def get_user(req: Request) -> Awaitable[OutUser]:
    tokens = get_tokens(req)
    with create_session() as session:
        user = (
            session.query(User).filter(User.access_token == tokens.access_token).first()
        )
        if user:
            return OutUser.from_orm(user)  # type: ignore
        raise DALError(HTTPStatus.UNAUTHORIZED.value)


async def check_auth(
    tokens: Tokens, need_user: bool = False, auth_redirect: bool = True
) -> Optional[OutUser]:
    access_token, refresh_token = tokens.access_token, tokens.refresh_token
    if not access_token and not refresh_token:
        if auth_redirect:
            raise NeedRedirectToLogin()
        raise AuthDataOutdated()
    if not access_token and refresh_token:
        if auth_redirect:
            await get_new_tokens(refresh_token)
        raise AuthDataOutdated()
    access_token = cast(str, access_token)
    try:
        user = await check_authorization(access_token)
        if not need_user:
            raise RedirectToUser(user=user)
        return user
    except AccessTokenOutdatedError:
        raise NeedRedirectToLogin()
    except DALError:
        if not auth_redirect:
            raise AuthDataOutdated()
        await get_new_tokens(refresh_token)


async def get_new_tokens(refresh_token) -> None:
    try:
        new_pair = await auth.refresh_tokens(refresh_token)
    except DALError:
        raise NeedRedirectToLogin()
    raise NeedRedirectToRefreshToken(tokens=new_pair)
