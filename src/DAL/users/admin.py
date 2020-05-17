from dataclasses import dataclass
from typing import Optional, TypeVar

from src.DAL.registration import (
    AbstractRegistration,
    SimpleRegistration,
    SimpleRegistrationParams,
)
from src.DAL.users.user import User
from src.DAL.users_dal import UsersDAL
from src.DAL.utils import ListWithPagination
from src.database.user_roles import UserRole
from src.models import (
    OperatorOut,
    OperatorToRegisterOut,
    OutUser,
    SecurityOut,
    SecurityToRegisterOut,
)


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
    async def get_operators(
        page: int, substring: Optional[str], size: int = 10
    ) -> ListWithPagination[OperatorOut]:
        return await UsersDAL.get_users(
            page, size, substring, OperatorOut, UserRole.OPERATOR
        )

    @staticmethod
    async def get_securities(
        page: int, substring: Optional[str], size: int = 10
    ) -> ListWithPagination[SecurityOut]:
        return await UsersDAL.get_users(
            page, size, substring, SecurityOut, UserRole.SECURITY
        )

    @staticmethod
    async def get_operators_to_register(
        page: int, substring: Optional[str], size: int = 10
    ) -> ListWithPagination[OperatorToRegisterOut]:
        return await UsersDAL.get_users_to_register(
            page, size, substring, OperatorToRegisterOut, UserRole.OPERATOR
        )

    @staticmethod
    async def get_securities_to_register(
        page: int, substring: Optional[str], size: int = 10
    ) -> ListWithPagination[SecurityToRegisterOut]:
        return await UsersDAL.get_users_to_register(
            page, size, substring, SecurityToRegisterOut, UserRole.SECURITY
        )

    @staticmethod
    async def remove_user_to_register(uuid: str) -> None:
        return await UsersDAL.remove_user_to_register(uuid)
