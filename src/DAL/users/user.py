from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Awaitable, Generic, TypeVar

from sqlalchemy.orm import Session
from src.database.database import create_session, run_in_threadpool
from src.database.models import User as DBUser
from src.exceptions import DALError
from src.messages import Message
from src.models import OutUser, UserWithTokens

TRegisterParams = TypeVar('TRegisterParams')


class User(ABC, Generic[TRegisterParams]):
    @staticmethod
    def _get_user(user_id: int, session: Session) -> DBUser:
        user = session.query(DBUser).filter(DBUser.id == user_id).one()
        if user:
            return user
        raise DALError(HTTPStatus.NOT_FOUND.value, Message.USER_DOES_NOT_EXISTS.value)

    @staticmethod
    @run_in_threadpool
    def get_user_tokens(user_id: int) -> Awaitable[UserWithTokens]:
        with create_session() as session:
            return UserWithTokens.from_orm(User._get_user(user_id, session))  # type: ignore

    @abstractmethod
    async def register_user(self, params: TRegisterParams) -> OutUser:
        pass
