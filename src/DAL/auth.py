from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, Awaitable, Dict, Optional

import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from src.config import tokens_settings
from src.controller.grant_type import GrantType
from src.DAL.password import get_password_hash
from src.DAL.user import User
from src.database.database import create_session, run_in_threadpool
from src.database.models import User as UserDB
from src.exceptions import AccessTokenOutdatedError, DALError
from src.messages import Message
from src.models import OutUser, TokensResponse, UserWithTokens

SECRET_KEY = '123'
ALGORITHM = 'HS256'
TOKEN_TYPE = 'bearer'
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth')


async def _get_user_from_db(user_id: int) -> UserWithTokens:
    user = await (User.get_user_tokens(user_id))
    return user


def _get_user_id(token: str) -> int:
    try:
        payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        if not user_id or not isinstance(user_id, int):
            raise DALError(
                HTTPStatus.BAD_REQUEST.value, Message.NOT_EXPECTING_PAYLOAD.value
            )
        return user_id
    except PyJWTError:
        raise DALError(
            HTTPStatus.BAD_REQUEST.value, Message.COULD_NOT_VALIDATE_CREDENTIALS.value
        )


def _is_valid_token(actual_token: str, expected_token: str) -> bool:
    return actual_token == expected_token


async def check_authorization(token: str) -> OutUser:
    '''
    Обрабатывает jwt
    :raises HttpException со статусом 401 если произошла ошибка при обработке токена
    :return: user
    '''
    user_id = _get_user_id(token)
    user = await _get_user_from_db(user_id)
    if _is_valid_token(token, user.access_token.decode()):
        return OutUser.parse_obj(user)
    raise AccessTokenOutdatedError(
        HTTPStatus.BAD_REQUEST.value, Message.ACCESS_TOKEN_OUTDATED.value
    )


def _is_password_correct(password: str, expected_password_hash: str) -> bool:
    return get_password_hash(password) == expected_password_hash


@run_in_threadpool
def _authenticate_user(username: str, password: str) -> Awaitable[OutUser]:
    message = Message.INCORRECT_USERNAME_OR_PASSWORD.value
    with create_session() as session:
        user: Optional[UserDB] = session.query(UserDB).filter(
            UserDB.username == username
        ).first()
        if user is None:
            raise DALError(HTTPStatus.NOT_FOUND.value, message)
        if _is_password_correct(password, user.password_hash):
            return OutUser.from_orm(user)  # type: ignore
        raise DALError(HTTPStatus.NOT_FOUND.value, message)


def _create_token(user_id: int, expires_delta: timedelta) -> bytes:
    expires_in = datetime.utcnow() + expires_delta
    payload: Dict[str, Any] = {'sub': user_id, 'exp': expires_in}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@run_in_threadpool
def _save_tokens_to_db(
    user: OutUser, access_token: bytes, refresh_token: bytes
) -> None:
    with create_session() as session:
        user_from_db = session.query(UserDB).filter(UserDB.id == user.id).one()
        user_from_db.refresh_token = refresh_token.decode()
        user_from_db.access_token = access_token.decode()
        session.add(user_from_db)


async def _create_tokens(user: OutUser) -> TokensResponse:
    access_token = _create_token(
        user.id, timedelta(minutes=tokens_settings.access_token_expire_minutes)
    )
    refresh_token = _create_token(
        user.id, timedelta(days=tokens_settings.refresh_toke_expire_time_days)
    )

    await _save_tokens_to_db(user, access_token, refresh_token)
    return TokensResponse(
        access_token=access_token, refresh_token=refresh_token, token_type=TOKEN_TYPE
    )


async def generate_tokens(username: str, password: str) -> TokensResponse:
    '''
    Создает access и refresh токены
    '''
    user = await _authenticate_user(username, password)
    return await _create_tokens(user)


async def refresh_tokens(refresh_token: str) -> TokensResponse:
    '''
    Проверяет refresh_token и возвращает новую пару токенов
    '''
    user_id = _get_user_id(refresh_token)
    user = await _get_user_from_db(user_id)
    if not _is_valid_token(refresh_token, user.refresh_token.decode()):
        raise DALError(
            HTTPStatus.BAD_REQUEST.value, Message.INVALID_REFRESH_TOKEN.value
        )
    return await _create_tokens(user)


async def authorize(
    grant_type: GrantType,
    username: Optional[str],
    password: Optional[str],
    refresh_token: Optional[str],
) -> TokensResponse:
    if grant_type == GrantType.refresh:
        if refresh_token:
            return await refresh_tokens(refresh_token)
    if grant_type == GrantType.password:
        if username and password:
            return await generate_tokens(username, password)
    raise DALError(
        HTTPStatus.UNAUTHORIZED.value, Message.INVALID_PARAMS_FOR_GETTING_TOKEN.value
    )
