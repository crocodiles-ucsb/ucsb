from abc import ABC, abstractmethod
from dataclasses import dataclass
from http import HTTPStatus
from typing import Awaitable, Generic

from sqlalchemy.exc import IntegrityError
from src.DAL.password import get_password_hash
from src.DAL.users.user import TRegisterParams
from src.DAL.utils import get_db_obj
from src.database.database import create_session, run_in_threadpool
from src.database.models import UserToRegister
from src.database.user_roles import UserRole
from src.exceptions import DALError
from src.messages import Message
from src.models import OutUser


@dataclass
class SimpleRegistrationParams:
    username: str
    password: str
    type: UserRole


@dataclass
class UniqueLinkRegistrationParams:
    username: str
    password: str
    type: UserRole
    uuid: str


class AbstractRegistration(Generic[TRegisterParams], ABC):
    @abstractmethod
    def register(self, params: TRegisterParams) -> Awaitable[OutUser]:
        pass


class SimpleRegistration(AbstractRegistration[SimpleRegistrationParams]):
    @run_in_threadpool
    def register(self, params: SimpleRegistrationParams) -> Awaitable[OutUser]:
        with create_session() as session:
            password_hash = get_password_hash(params.password)
            db_obj = get_db_obj(params.type)
            user = db_obj(
                username=params.username,
                password_hash=password_hash,
                type=params.type.value,
            )
            session.add(user)
            try:
                session.flush()
            except IntegrityError:
                raise DALError(
                    HTTPStatus.BAD_REQUEST.value, Message.USER_ALREADY_EXISTS.value
                )
            return OutUser.from_orm(user)  # type: ignore


class RegistrationViaUniqueLink(AbstractRegistration[UniqueLinkRegistrationParams]):
    @staticmethod
    @run_in_threadpool
    def is_valid_uuid(uuid: str) -> bool:
        with create_session() as session:
            return (
                session.query(UserToRegister)
                .filter(UserToRegister.uuid == uuid)
                .first()
            )

    @run_in_threadpool
    def register(self, params: UniqueLinkRegistrationParams) -> Awaitable[OutUser]:
        pass
