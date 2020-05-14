from http import HTTPStatus

import pytest
from src.DAL.adding_user import AbstractAddingUser
from src.DAL.registration import (
    RegistrationViaUniqueLink,
    SimpleRegistration,
    UniqueLinkRegistrationParams,
)
from src.DAL.users.operator import OperatorToAddingOut
from src.database.database import create_session
from src.database.models import Operator, User
from src.database.user_roles import UserRole
from src.exceptions import DALError
from src.messages import Message


@pytest.mark.asyncio
@pytest.mark.usefixtures('_add_user')
async def test_simple_registration_adds_user_to_db(simple_registration_params):
    with create_session() as session:
        user = session.query(User).filter(User.id == 1).one()
        assert user.type == simple_registration_params.type.value
        assert user.username == simple_registration_params.username


@pytest.mark.asyncio
async def test_simple_registration_returns_expected_value(
    simple_registration_params, simple_registration: SimpleRegistration
):
    res = await simple_registration.register(simple_registration_params)
    assert res.username == simple_registration_params.username
    assert res.type == simple_registration_params.type.value
    assert res.id == 1


@pytest.mark.asyncio
@pytest.mark.usefixtures('_add_user')
async def test_simple_registration_raises_error_if_user_exists(
    simple_registration_params, simple_registration
):
    with pytest.raises(DALError) as e:
        await simple_registration.register(simple_registration_params)
    assert e.value.status_code == HTTPStatus.BAD_REQUEST.value


@pytest.fixture()
def uuid():
    return 'test_uuid'


@pytest.fixture()
async def operator_to_register_uuid(
    operator_adding_params, adding_user_with_disposable_link: AbstractAddingUser
):
    res = await adding_user_with_disposable_link.add_user(
        UserRole.OPERATOR, operator_adding_params, OperatorToAddingOut
    )
    return res.uuid


@pytest.fixture()
async def unique_link_registration_params(operator_to_register_uuid):
    return UniqueLinkRegistrationParams(
        username='123', password='123', uuid=operator_to_register_uuid,
    )


@pytest.fixture()
def registration_via_unique_link():
    return RegistrationViaUniqueLink()


@pytest.mark.asyncio
async def test_registration_via_unique_link_returns_expecting_value(
    registration_via_unique_link,
    unique_link_registration_params: UniqueLinkRegistrationParams,
):
    res = await registration_via_unique_link.register(unique_link_registration_params)
    assert res.username == unique_link_registration_params.username
    assert res.type == UserRole.OPERATOR.value


@pytest.mark.asyncio
async def test_registration_via_unique_link_saves_data_to_db(
    registration_via_unique_link,
    unique_link_registration_params: UniqueLinkRegistrationParams,
    operator_adding_params,
):
    await registration_via_unique_link.register(unique_link_registration_params)
    with create_session() as session:
        operator = session.query(Operator).filter(Operator.id == 1).one()
        assert operator.last_name == operator_adding_params.last_name
        assert operator.type == UserRole.OPERATOR.value
        assert operator.username == unique_link_registration_params.username


@pytest.mark.asyncio
async def test_link_will_be_non_working_after_registration(
    registration_via_unique_link,
    unique_link_registration_params: UniqueLinkRegistrationParams,
    operator_adding_params,
):
    await registration_via_unique_link.register(unique_link_registration_params)
    with pytest.raises(DALError) as e:
        await registration_via_unique_link.register(unique_link_registration_params)
    value = e.value
    assert value.detail == Message.LINK_INVALID_OR_OUTDATED.value
    assert value.status_code == HTTPStatus.BAD_REQUEST.value


@pytest.mark.asyncio
async def test_registration_via_unique_link_when_uuid_is_invalid_raises_error(
    registration_via_unique_link,
    unique_link_registration_params: UniqueLinkRegistrationParams,
    operator_adding_params,
    uuid,
):
    unique_link_registration_params.uuid = uuid
    with pytest.raises(DALError) as e:
        await registration_via_unique_link.register(unique_link_registration_params)
    value = e.value
    assert value.status_code == HTTPStatus.BAD_REQUEST.value
    assert value.detail == Message.LINK_INVALID_OR_OUTDATED.value
