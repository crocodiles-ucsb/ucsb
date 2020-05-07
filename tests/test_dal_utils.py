import pytest
from src.DAL.utils import get_url_postfix
from src.database.user_roles import UserRole
from src.models import OutUser


@pytest.fixture()
def username():
    return '1'


@pytest.mark.parametrize(
    'user_id, user_type, postfix',
    [
        (1, UserRole.ADMIN.value, '/admins/1'),
        (2, UserRole.ADMIN.value, '/admins/2'),
        (3, UserRole.OPERATOR.value, '/operators/3'),
        (3, UserRole.SECURITY.value, '/securities/3'),
        (3, UserRole.CONTRACTOR_REPRESENTATIVE.value, '/Contractor representatives/3'),
    ],
)
def test_get_user_role(user_id, user_type, postfix, username):
    user = OutUser(id=user_id, type=user_type, username=username)
    assert get_url_postfix(user) == postfix
