from typing import List

import pytest
from src.DAL.utils import ListWithPagination, get_pagination, get_url_postfix
from src.database.user_roles import UserRole
from src.exceptions import DALError
from src.models import OutUser


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


@pytest.mark.parametrize(
    ('size', 'page', 'expected_size'), [(15, 1, 15), (8, 2, 7), (20, 1, 15)]
)
def test_pagination(size: int, page: int, expected_size: int):
    count_of_operations: int = 15
    objects: List[int] = [None] * count_of_operations
    for i in range(count_of_operations):
        objects[i] = i
    res: ListWithPagination[int] = get_pagination(objects, page=page, size=size)
    assert len(res.data) == expected_size


def test_pagination_will_not_raise_error_when_no_elements_in_list():
    res = get_pagination([], 1, 10)
    assert res.data == []


def test_pagination_with_invalid_size_and_page():
    with pytest.raises(DALError):
        get_pagination([], 0, 0)


@pytest.fixture()
def fifteen_numbers():
    return [i for i in range(15)]


def test_pagination_params_on_first_page_when_next_page_exists(fifteen_numbers):
    res = get_pagination(fifteen_numbers, 1, 2)
    params = res.pagination_params
    assert params.current_page == 1
    assert not params.has_prev_page
    assert params.has_next_page
    assert params.next_page == 2


def test_pagination_params_on_second_page_when_next_page_exists(fifteen_numbers):
    res = get_pagination(fifteen_numbers, 2, 2)
    params = res.pagination_params
    assert params.has_next_page
    assert params.has_prev_page
    assert params.current_page == 2
    assert params.prev_page == 1
    assert params.next_page == 3


def test_pagination_params_on_single_page(fifteen_numbers):
    res = get_pagination(fifteen_numbers, 1, 15)
    params = res.pagination_params
    assert not params.has_next_page
    assert not params.has_prev_page
    assert params.current_page == 1
