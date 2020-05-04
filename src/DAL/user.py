from typing import Awaitable

from sqlalchemy.orm import Session
from src.database.database import create_session, run_in_threadpool
from src.database.models import User
from src.exceptions import DALError
from src.messages import Message
from src.models import UserWithTokens


def _get_user(user_id: int, session: Session) -> User:
    user = session.query(User).filter(User.id == user_id).one()
    if user:
        return user
    raise DALError(Message.USER_DOES_NOT_EXISTS.value)


@run_in_threadpool
def get_user_with_tokens(user_id: int) -> Awaitable[UserWithTokens]:
    with create_session() as session:
        return UserWithTokens.from_orm(_get_user(user_id, session))  # type: ignore
