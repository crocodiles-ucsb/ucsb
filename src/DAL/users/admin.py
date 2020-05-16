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
from src.models import OperatorOut, OutUser, SecurityOut, OperatorToRegisterOut, SecurityToRegisterOut


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

    @staticmethod
    async def get_operators(page: int, size: int = 10) -> List[OperatorOut]:
        return await UsersDAL.get_users(page, size, OperatorOut, UserRole.OPERATOR)

    @staticmethod
    async def get_securities(page: int, size: int = 10) -> List[SecurityOut]:
        return await UsersDAL.get_users(page, size, SecurityOut, UserRole.SECURITY)

    @staticmethod
    async def get_operators_to_register(page: int, size: int = 10) -> List[OperatorToRegisterOut]:
        return await UsersDAL.get_users_to_register(page, size, OperatorToRegisterOut, UserRole.OPERATOR)

    @staticmethod
    async def get_securities_to_register(page: int, size: int = 10) -> List[SecurityToRegisterOut]:
        return await UsersDAL.get_users_to_register(page, size, SecurityToRegisterOut, UserRole.SECURITY)

    @staticmethod
    async def remove_user_to_register(uuid: str) -> None:
        return await UsersDAL.remove_user_to_register(uuid)
