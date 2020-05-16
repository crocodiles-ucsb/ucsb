from http import HTTPStatus
from io import StringIO
from typing import List, Type, TypeVar

from src.database.models import (
    Admin,
    ContractorRepresentative,
    ContractorRepresentativeToRegister,
    Operator,
    OperatorToRegister,
    Security,
    SecurityToRegister,
    User,
    UserToRegister,
)
from src.database.user_roles import UserRole
from src.exceptions import DALError
from src.messages import Message
from src.models import OutUser
from src.urls import Urls


def get_url_postfix(user: OutUser) -> str:
    res = StringIO()
    res.write('/')
    if user.type == UserRole.SECURITY.value:
        res.write(user.type[:-1])
        res.write('ies')
    else:
        res.write(user.type)
        res.write('s')
    res.write('/')
    res.write(str(user.id))
    return res.getvalue()


def get_registration_url(uuid: str) -> str:
    return f'{Urls.registration_url}/{uuid}'


def get_db_obj(user_role: UserRole) -> Type[User]:
    if user_role == UserRole.ADMIN:
        return Admin
    if user_role == UserRole.OPERATOR:
        return Operator
    if user_role == UserRole.CONTRACTOR_REPRESENTATIVE:
        return ContractorRepresentative
    if user_role == UserRole.SECURITY:
        return Security
    raise ValueError()


def get_obj_from_obj_to_register(user_to_register: UserToRegister) -> Type[User]:
    if isinstance(user_to_register, OperatorToRegister):
        return Operator
    if isinstance(user_to_register, SecurityToRegister):
        return Security
    raise ValueError()


def get_db_obj_to_register(user_role: UserRole) -> Type[UserToRegister]:
    if user_role == UserRole.OPERATOR:
        return OperatorToRegister
    if user_role == UserRole.SECURITY:
        return SecurityToRegister
    if user_role == UserRole.CONTRACTOR_REPRESENTATIVE:
        return ContractorRepresentativeToRegister
    raise ValueError()


T = TypeVar('T')


def get_pagination(objects: List[T], page: int, size: int) -> List[T]:
    start_index: int = 0
    if page < 1 or size < 1 or page * size > len(objects) + size:
        raise DALError(
            HTTPStatus.BAD_REQUEST.value, Message.INVALID_PAGINATION_PARAMS.value
        )
    if page > 1:
        start_index = (page - 1) * size
    end_index: int = start_index + size - 1
    length = len(objects)
    if end_index >= length:
        end_index = length - 1
    res: List[T] = []
    for i in range(start_index, end_index + 1):
        res.append(objects[i])
    return res
