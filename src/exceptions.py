from fastapi import HTTPException


class DALError(HTTPException):
    pass
