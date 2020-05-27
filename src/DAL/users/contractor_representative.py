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


class ContractorRepresentativeToAddingOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    telephone_number: str
    email: str
    uuid: str

    class Config:
        orm_mode = True


class ContractorRepresentativeAddingParams(BaseModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    telephone_number: str
    email: str
    contractor_id: int


class ContractorRepresentatives(
    SimpleUser[
        ContractorRepresentativeAddingParams,
        ContractorRepresentativeToAddingOut,
        UniqueLinkRegistrationParams,
    ]
):
    def __init__(self) -> None:
        self.adding_user: AbstractAddingUser[
            ContractorRepresentativeAddingParams, ContractorRepresentativeToAddingOut
        ] = AddingUserWithDisposableLink[
            ContractorRepresentativeAddingParams, ContractorRepresentativeToAddingOut
        ]()
        self.registration_user: AbstractRegistration[
            UniqueLinkRegistrationParams
        ] = RegistrationViaUniqueLink()

    async def add_user(
        self, params: ContractorRepresentativeAddingParams
    ) -> ContractorRepresentativeToAddingOut:
        return await self.adding_user.add_user(
            UserRole.CONTRACTOR_REPRESENTATIVE,
            params,
            ContractorRepresentativeToAddingOut,
        )

    async def register_user(self, params: UniqueLinkRegistrationParams) -> OutUser:
        return await self.registration_user.register(params)
