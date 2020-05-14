from typing import Optional

from pydantic import BaseModel
from src.DAL.adding_user import AbstractAddingUser, AddingUserWithDisposableLink
from src.DAL.registration import (
    AbstractRegistration,
    RegistrationViaUniqueLink,
    UniqueLinkRegistrationParams,
)
from src.DAL.users.simple_user import SimpleUser, TAddingUserParams
from src.database.user_roles import UserRole
from src.models import OutUser


class OperatorToAddingOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    uuid: str

    class Config:
        orm_mode = True


class OperatorAddingParams(BaseModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None


class Operator(
    SimpleUser[OperatorAddingParams, OperatorToAddingOut, UniqueLinkRegistrationParams]
):
    def __init__(self) -> None:
        self.adding_user: AbstractAddingUser[
            OperatorAddingParams, OperatorToAddingOut
        ] = AddingUserWithDisposableLink[OperatorAddingParams, OperatorToAddingOut]()
        self.registration_user: AbstractRegistration[
            UniqueLinkRegistrationParams
        ] = RegistrationViaUniqueLink()

    async def add_user(self, params: TAddingUserParams) -> OperatorToAddingOut:
        return await self.adding_user.add_user(
            UserRole.OPERATOR, params, OperatorToAddingOut
        )

    async def register_user(self, params: UniqueLinkRegistrationParams) -> OutUser:
        return await self.registration_user.register(params)
