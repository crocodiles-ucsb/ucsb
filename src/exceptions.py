from fastapi import HTTPException
from starlette.requests import Request


class DALError(HTTPException):
    pass


class NeedRedirectToLogin(Exception):
    pass


class AccessForbidden(Exception):
    def __init__(self, request: Request):
        super().__init__()
        self.request: Request = request
