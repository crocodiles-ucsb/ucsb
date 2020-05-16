from http import HTTPStatus
from typing import Awaitable, Type, TypeVar

from src.DAL.utils import (
    ListWithPagination,
    Pagination,
    get_db_obj_to_register,
    get_pagination,
)
from src.database.database import create_session, run_in_threadpool
from src.database.models import User, UserToRegister
from src.database.user_roles import UserRole
from src.exceptions import DALError
from src.messages import Message


class UsersDAL:
    TOutModel = TypeVar('TOutModel')

    @staticmethod
    @run_in_threadpool
    def get_users(
        page: int, size: int, out_model: Type[TOutModel], user_type: UserRole
    ) -> Awaitable[ListWithPagination[TOutModel]]:
        with create_session() as session:
            users = session.query(User).filter(User.type == user_type.value).all()
            users = [out_model.from_orm(user) for user in users]
        return get_pagination(users, page, size)  # type : ignore

    @staticmethod
    @run_in_threadpool
    def get_users_to_register(
        page: int, size: int, out_model: Type[TOutModel], user_type: UserRole
    ) -> Awaitable[ListWithPagination[TOutModel]]:
        with create_session() as session:
            obj = get_db_obj_to_register(user_type)
            users_to_register = session.query(obj).all()
            users = [out_model.from_orm(user) for user in users_to_register]
        return get_pagination(users, page, size)  # type: ignore

    @staticmethod
    @run_in_threadpool
    def remove_user_to_register(uuid: str) -> None:
        with create_session() as session:
            user = (
                session.query(UserToRegister)
                .filter(UserToRegister.uuid == uuid)
                .first()
            )
            if not user:
                raise DALError(
                    HTTPStatus.BAD_REQUEST.value, Message.USER_DOES_NOT_EXISTS.value
                )
            session.delete(user)
