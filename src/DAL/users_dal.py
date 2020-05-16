from typing import Awaitable, List, TypeVar, Type

from src.DAL.utils import get_pagination
from src.database.database import create_session, run_in_threadpool
from src.database.models import User
from src.database.user_roles import UserRole


class UsersDAL:
    TOutModel = TypeVar('TOutModel')

    @staticmethod
    @run_in_threadpool
    def get_users(
        page: int, size: int, out_model: TOutModel, user_type: UserRole
    ) -> Awaitable[List[TOutModel]]:
        with create_session() as session:
            users = session.query(User).filter(User.type == user_type.value).all()
            users = get_pagination(users, page, size)
            return [out_model.from_orm(user) for user in users]  # type : ignore
