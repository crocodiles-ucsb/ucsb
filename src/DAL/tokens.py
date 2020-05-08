from typing import Optional, cast

from src.DAL import auth
from src.DAL.auth import check_authorization
from src.DAL.utils import Tokens
from src.exceptions import (
    AccessTokenOutdatedError,
    DALError,
    NeedRedirectToLogin,
    NeedRedirectToRefreshToken,
    RedirectToUser,
)
from src.models import OutUser


async def check_auth(tokens: Tokens, need_user: bool = False) -> Optional[OutUser]:
    access_token, refresh_token = tokens.access_token, tokens.refresh_token
    if not access_token and not refresh_token:
        raise NeedRedirectToLogin()
    if not access_token and refresh_token:
        await get_new_tokens(refresh_token)
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
