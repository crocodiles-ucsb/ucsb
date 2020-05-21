from typing import Optional

from pydantic import BaseModel


class TokensResponse(BaseModel):
    token_type: str
    access_token: bytes
    refresh_token: bytes


class InUser(BaseModel):
    username: str
    password: str


class InUserWithUUID(InUser):
    uuid: str


class OutUser(BaseModel):
    id: int
    username: str
    type: str

    class Config:
        orm_mode = True


class MyModel(BaseModel):
    url: str


class UserWithTokens(OutUser):
    access_token: bytes
    refresh_token: bytes


class InRefreshToken(BaseModel):
    refresh_token: str


class OperatorIn(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None


class OperatorOut(OperatorIn):
    class Config:
        orm_mode = True


class SecurityIn(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    position: str


class SecurityOut(SecurityIn):
    class Config:
        orm_mode = True


class SecurityToRegisterOut(SecurityOut):
    uuid: str


class OperatorToRegisterOut(OperatorOut):
    uuid: str


class SimpleCatalogOut(BaseModel):
    id: int
    data: str

    class Config:
        orm_mode = True


class CatalogWithIntValueOut(SimpleCatalogOut):
    value: int


class SimpleCatalogIn(BaseModel):
    data: str


class CatalogWithIntValueIn(SimpleCatalogIn):
    value: int
