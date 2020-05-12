from dataclasses import dataclass
from typing import Optional, cast

from src.DAL import auth
from src.DAL.auth import check_authorization
from src.exceptions import (
    AccessTokenOutdatedError,
    DALError,
    NeedRedirectToLogin,
    NeedRedirectToRefreshToken,
    RedirectToUser,
    AuthDataOutdated)
from src.models import OutUser
from starlette.requests import Request


@dataclass
class Tokens:
    access_token: Optional[str]
    refresh_token: Optional[str]


def get_tokens(req: Request) -> Tokens:
    cookies = req.cookies
    return Tokens(cookies.get('access_token'), cookies.get('refresh_token'))


async def check_auth(tokens: Tokens, need_user: bool = False, auth_redirect: bool = True) -> Optional[OutUser]:
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
        await get_new_tokens(refresh_token)


async def get_new_tokens(refresh_token) -> None:
    try:
        new_pair = await auth.refresh_tokens(refresh_token)
    except DALError:
        raise NeedRedirectToLogin()
    raise NeedRedirectToRefreshToken(tokens=new_pair)
