from dataclasses import dataclass
from typing import TypeVar

from src.DAL.registration import (
    AbstractRegistration,
    SimpleRegistration,
    SimpleRegistrationParams,
)
from src.DAL.users.user import User
from src.models import OutUser


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
