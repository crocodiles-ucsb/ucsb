from src.DAL.adding_user import AbstractAddingUser, AddingUserWithDisposableLink
from src.DAL.users.simple_user import SimpleUser, TAddingUserParams
from src.DAL.users.user import TRegisterParams
from src.database.user_roles import UserRole
from src.models import OperatorAddingParams, OperatorToRegisterOut, OutUser


class Operator(SimpleUser[OperatorAddingParams, OperatorToRegisterOut]):

    def __init__(self) -> None:
        self.adding_user: AbstractAddingUser[
            OperatorAddingParams, OperatorToRegisterOut
        ] = AddingUserWithDisposableLink[OperatorAddingParams, OperatorToRegisterOut]()

    async def add_user(self, params: TAddingUserParams) -> OperatorToRegisterOut:
        return await self.adding_user.add_user(UserRole.OPERATOR, params, OperatorToRegisterOut)

    async def register_user(self, params: TRegisterParams) -> OutUser:
        pass
