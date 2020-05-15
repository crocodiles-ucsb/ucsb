from typing import Optional

from pydantic import BaseModel
from src.DAL.adding_user import AbstractAddingUser, AddingUserWithDisposableLink
from src.DAL.registration import (
    AbstractRegistration,
    RegistrationViaUniqueLink,
    UniqueLinkRegistrationParams,
)
from src.DAL.users.simple_user import SimpleUser
from src.database.user_roles import UserRole
from src.models import OutUser


class SecurityToAddingOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    position: str
    uuid: str

    class Config:
        orm_mode = True


class SecurityAddingParams(BaseModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    position: str


class Security(
    SimpleUser[SecurityAddingParams, SecurityToAddingOut, UniqueLinkRegistrationParams]
):
    def __init__(self) -> None:
        self.adding_user: AbstractAddingUser[
            SecurityAddingParams, SecurityToAddingOut
        ] = AddingUserWithDisposableLink[SecurityAddingParams, SecurityToAddingOut]()
        self.registration_user: AbstractRegistration[
            UniqueLinkRegistrationParams
        ] = RegistrationViaUniqueLink()

    async def add_user(self, params: SecurityAddingParams) -> SecurityToAddingOut:
        return await self.adding_user.add_user(
            UserRole.SECURITY, params, SecurityToAddingOut
        )

    async def register_user(self, params: UniqueLinkRegistrationParams) -> OutUser:
        return await self.registration_user.register(params)
