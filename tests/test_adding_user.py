import pytest
from src.DAL.adding_user import AddingUserWithDisposableLink
from src.DAL.users.operator import OperatorAddingParams, OperatorToAddingOut
from src.database.database import create_session
from src.database.models import OperatorToRegister
from src.database.user_roles import UserRole


@pytest.fixture()
def mocked_uuid(mocker):
    return mocker.patch('src.DAL.adding_user.uuid')


@pytest.mark.asyncio
async def test_adding_user_with_disposable_link_returns_expecting_value(
    adding_user_with_disposable_link: AddingUserWithDisposableLink[
        OperatorAddingParams, OperatorToAddingOut
    ],
    operator_adding_params,
    mocked_uuid,
):
    mocked_uuid.uuid4.return_value = '123'
    res = await adding_user_with_disposable_link.add_user(
        UserRole.OPERATOR, operator_adding_params, OperatorToAddingOut
    )
    assert res.last_name == operator_adding_params.last_name
    assert res.uuid == '123'


@pytest.mark.asyncio
async def test_adding_user_with_disposable_link_saves_data_to_db(
    adding_user_with_disposable_link: AddingUserWithDisposableLink[
        OperatorAddingParams, OperatorToAddingOut
    ],
    operator_adding_params,
    mocked_uuid,
):
    mocked_uuid.uuid4.return_value = '123'
    await adding_user_with_disposable_link.add_user(
        UserRole.OPERATOR, operator_adding_params, OperatorToAddingOut
    )
    with create_session() as session:
        res = session.query(OperatorToRegister).filter(OperatorToRegister.id == 1).one()
        assert res.uuid == '123'
        assert res.last_name == res.last_name
