from http import HTTPStatus

import pytest
from src.DAL.registration import (
    AbstractRegistration,
    SimpleRegistration,
    SimpleRegistrationParams,
)
from src.database.database import create_session
from src.database.models import User
from src.exceptions import DALError


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
