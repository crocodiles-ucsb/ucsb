from typing import Optional

from fastapi import HTTPException
from src.models import OutUser, TokensResponse
from starlette.requests import Request


class DALError(HTTPException):
    pass


class NeedRedirectToLogin(Exception):
    pass


class AccessForbidden(Exception):
    pass


class AccessTokenOutdatedError(Exception):
    pass


class AuthDataOutdated(Exception):
    pass


class NeedRedirectToRefreshToken(Exception):
    def __init__(self, tokens: TokensResponse, req: Optional[Request] = None):
        super().__init__()
        self.tokens: TokensResponse = tokens
        self.request: Optional[Request] = req


class RedirectToUser(Exception):
    def __init__(self, user: OutUser):
        super().__init__()
        self.user: OutUser = user
