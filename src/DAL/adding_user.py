import uuid
from abc import ABC, abstractmethod
from typing import Awaitable, Generic, Type, TypeVar

from src.DAL.utils import get_db_obj_to_register
from src.database.database import create_session, run_in_threadpool
from src.database.models import UserToRegister
from src.database.user_roles import UserRole

TAddingUserParams = TypeVar('TAddingUserParams')
TAddingUserOut = TypeVar('TAddingUserOut')


class AbstractAddingUser(Generic[TAddingUserParams, TAddingUserOut], ABC):
    @abstractmethod
    async def add_user(
        self, role: UserRole, params: TAddingUserParams, out_model: Type[TAddingUserOut]
    ) -> TAddingUserOut:
        pass

    T = TypeVar('T', bound=UserToRegister)

    @run_in_threadpool
    def _add_db_obj_to_register_to_db(
        self, obj: T, out_model: Type[TAddingUserOut]
    ) -> Awaitable[TAddingUserOut]:
        with create_session() as session:
            session.add(obj)
            session.flush()
            return out_model.from_orm(obj)  # type: ignore


class AddingUserWithDisposableLink(
    Generic[TAddingUserParams, TAddingUserOut],
    AbstractAddingUser[TAddingUserParams, TAddingUserOut],
):
    async def add_user(
        self, role: UserRole, params: TAddingUserParams, out_model: Type[TAddingUserOut]
    ) -> TAddingUserOut:
        db_obj_to_register = get_db_obj_to_register(role)
        obj = db_obj_to_register(**params.__dict__, uuid=str(uuid.uuid4()))
        return await self._add_db_obj_to_register_to_db(obj, out_model)
