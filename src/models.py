from pydantic import BaseModel
from src.database.user_roles import UserRole


class TokensResponse(BaseModel):
    token_type: str
    access_token: bytes
    refresh_token: bytes


class InUser(BaseModel):
    username: str
    password: str


class OutUser(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserWithRole(BaseModel):
    role: UserRole


class UserWithTokens(OutUser):
    access_token: bytes
    refresh_token: bytes


class InRefreshToken(BaseModel):
    refresh_token: str
