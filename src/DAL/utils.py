from io import StringIO
from typing import Type

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
