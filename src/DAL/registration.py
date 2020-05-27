from abc import ABC, abstractmethod
from dataclasses import dataclass
from http import HTTPStatus
from typing import Awaitable, Generic, Optional, Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.DAL.password import get_password_hash
from src.DAL.users.user import TRegisterParams
from src.DAL.utils import get_db_obj, get_obj_from_obj_to_register
from src.database.database import create_session, run_in_threadpool
from src.database.models import (
    ContractorRepresentativeToRegister,
    OperatorToRegister,
    SecurityToRegister,
    User,
    UserToRegister,
)
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
    uuid: str


class AbstractRegistration(Generic[TRegisterParams], ABC):
    @abstractmethod
    def register(self, params: TRegisterParams) -> Awaitable[OutUser]:
        pass

    def _add_user(
        self, session: Session, username: str, password: str, db_obj: Type[User]
    ) -> User:
        password_hash = get_password_hash(password)
        user = db_obj(username=username, password_hash=password_hash,)
        session.add(user)
        try:
            session.flush()
        except IntegrityError as e:
            print(e)
            raise DALError(
                HTTPStatus.BAD_REQUEST.value, Message.USER_ALREADY_EXISTS.value
            )
        return user


class SimpleRegistration(AbstractRegistration[SimpleRegistrationParams]):
    @run_in_threadpool
    def register(self, params: SimpleRegistrationParams) -> Awaitable[OutUser]:
        with create_session() as session:
            user = self._add_user(
                session,
                username=params.username,
                password=params.password,
                db_obj=get_db_obj(params.type),
            )
            return OutUser.from_orm(user)  # type: ignore


class RegistrationViaUniqueLink(AbstractRegistration[UniqueLinkRegistrationParams]):
    @staticmethod
    @run_in_threadpool
    def is_valid_uuid(uuid: str) -> bool:
        with create_session() as session:
            return (
                RegistrationViaUniqueLink._get_user_to_register(session, uuid)
                is not None
            )

    @staticmethod
    def _get_user_to_register(session: Session, uuid: str) -> Optional[UserToRegister]:
        return session.query(UserToRegister).filter(UserToRegister.uuid == uuid).first()

    def _transfer_fields(self, obj: User, obj_to_register: UserToRegister) -> User:
        if isinstance(obj_to_register, OperatorToRegister):
            obj.last_name = obj_to_register.last_name
            obj.first_name = obj_to_register.first_name
            obj.patronymic = obj_to_register.patronymic
        elif isinstance(obj_to_register, SecurityToRegister):
            obj.last_name = obj_to_register.last_name
            obj.first_name = obj_to_register.first_name
            obj.patronymic = obj_to_register.patronymic
            obj.position = obj_to_register.position
        elif isinstance(obj_to_register, ContractorRepresentativeToRegister):
            obj.last_name = obj_to_register.last_name
            obj.first_name = obj_to_register.first_name
            obj.patronymic = obj_to_register.patronymic
            obj.email = obj_to_register.email
            obj.telephone_number = obj_to_register.telephone_number
            obj.contractor_id = obj_to_register.contractor_id
        return obj

    @run_in_threadpool
    def register(self, params: UniqueLinkRegistrationParams) -> Awaitable[OutUser]:
        with create_session() as session:
            user_to_register = self._get_user_to_register(session, params.uuid)
            if not user_to_register:
                raise DALError(
                    HTTPStatus.BAD_REQUEST.value, Message.LINK_INVALID_OR_OUTDATED.value
                )
            user = self._add_user(
                session,
                username=params.username,
                password=params.password,
                db_obj=get_obj_from_obj_to_register(user_to_register),
            )
            user = self._transfer_fields(user, user_to_register)
            session.delete(user_to_register)
            return OutUser.from_orm(user)  # type: ignore
