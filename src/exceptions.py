from fastapi import HTTPException
from src.models import OutUser, TokensResponse


class DALError(HTTPException):
    pass


class NeedRedirectToLogin(Exception):
    pass


class AccessForbidden(Exception):
    pass


class AccessTokenOutdatedError(Exception):
    pass


class NeedRedirectToRefreshToken(Exception):
    def __init__(self, tokens: TokensResponse):
        super().__init__()
        self.tokens: TokensResponse = tokens


class RedirectToUser(Exception):
    def __init__(self, user: OutUser):
        super().__init__()
        self.user: OutUser = user
