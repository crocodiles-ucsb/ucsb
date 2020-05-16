from dataclasses import dataclass
from typing import List, TypeVar

from src.DAL.registration import (
    AbstractRegistration,
    SimpleRegistration,
    SimpleRegistrationParams,
)
from src.DAL.users.user import User
from src.DAL.users_dal import UsersDAL
from src.database.user_roles import UserRole
from src.models import OperatorOut, OutUser, SecurityOut


@dataclass
class OperatorAddingParams:
    name: str


TUserParams = TypeVar('TUserParams')


class Admin(User[SimpleRegistrationParams]):
    def __init__(self) -> None:
        self.registration: AbstractRegistration[
            SimpleRegistrationParams
        ] = SimpleRegistration()

    async def register_user(self, params: SimpleRegistrationParams) -> OutUser:
        return await self.registration.register(params)

    async def get_operators(self, page: int, size: int = 10) -> List[OperatorOut]:
        return await UsersDAL.get_users(page, size, OperatorOut, UserRole.OPERATOR)

    async def get_securities(self, page: int, size: int = 10) -> List[SecurityOut]:
        return await UsersDAL.get_users(page, size, SecurityOut, UserRole.SECURITY)
