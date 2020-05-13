from http import HTTPStatus

import pytest
from mock import AsyncMock
from src.DAL.tokens import check_auth
from src.DAL.utils import Tokens
from src.database.user_roles import UserRole
from src.exceptions import (
    AccessTokenOutdatedError,
    DALError,
    NeedRedirectToLogin,
    NeedRedirectToRefreshToken,
    RedirectToUser,
)
from src.models import OutUser, TokensResponse, UserWithTokens


@pytest.fixture()
def mock__is_valid_token(mocker):
    return mocker.patch('src.DAL.auth._is_valid_token')


@pytest.fixture()
def mock__get_user_from_db(mocker):
    return mocker.patch('src.DAL.auth._get_user_from_db')


@pytest.fixture()
def mock__get_user_id(mocker):
    return mocker.patch('src.DAL.auth._get_user_id')


@pytest.fixture()
def token():
    return '1'


@pytest.fixture()
def out_user(username):
    return OutUser(id=1, username=username, type=UserRole.ADMIN.value)


@pytest.fixture()
def tokens_response(token):
    return TokensResponse(token_type='Bearer', access_token=token, refresh_token=token)


@pytest.fixture()
def user_with_tokens(out_user, token, tokens_response):
    return UserWithTokens(
        access_token=tokens_response.access_token,
        refresh_token=tokens_response.refresh_token,
        **out_user.dict()
    )


@pytest.fixture()
def tokens(token):
    return Tokens(token, token)


@pytest.mark.asyncio
@pytest.mark.usefixtures('mock__get_user_id')
async def test_check_auth_returns_user_when_token_is_valid(
    mock__get_user_from_db, mock__is_valid_token, tokens, user_with_tokens, out_user
):
    mock__is_valid_token.return_value = True
    mock__get_user_from_db.return_value = user_with_tokens
    with pytest.raises(RedirectToUser) as e:
        await check_auth(tokens)
    assert e.value.user == out_user


@pytest.mark.asyncio
@pytest.mark.usefixtures('mock__get_user_id', 'mock__get_user_from_db')
async def test_check_auth_returns_user_when_token_is_not_valid_and_refresh_is_valid(
    tokens_response, mock__is_valid_token, tokens, mock_auth
):
    mock_auth.refresh_tokens = AsyncMock(return_value=tokens_response)
    mock__is_valid_token.return_value = False
    with pytest.raises(NeedRedirectToLogin) as e:
        await check_auth(tokens)
    assert e.value


@pytest.mark.asyncio
@pytest.mark.usefixtures('mock__get_user_id', 'mock__get_user_from_db')
async def test_check_auth_returns_user_when_token_is_not_valid_and_refresh_is_not_valid_too(
    mock__is_valid_token, tokens,
):
    mock__is_valid_token.return_value = False
    with pytest.raises(NeedRedirectToLogin):
        await check_auth(tokens)


@pytest.mark.asyncio
async def test_check_auth_when_user_does_not_have_tokens_raises_need_redirect():
    with pytest.raises(NeedRedirectToLogin):
        await check_auth(Tokens(None, None))


@pytest.fixture()
def mock_auth(mocker):
    return mocker.patch('src.DAL.tokens.auth')


@pytest.mark.asyncio
async def test_check_auth_when_user_has_breathe_refresh_token_raises_need_redirect_to_refresh(
    token, mock_auth, tokens_response
):
    mock_auth.refresh_tokens = AsyncMock(return_value=tokens_response)
    with pytest.raises(NeedRedirectToRefreshToken) as e:
        await check_auth(Tokens(None, token))
    assert e.value.tokens == tokens_response


@pytest.mark.asyncio
async def test_check_auth_when_user_has_old_refresh_token_raises_need_login(
    token, mock_auth
):
    mock_auth.refresh_tokens = AsyncMock(
        side_effect=DALError(HTTPStatus.BAD_REQUEST.value)
    )
    with pytest.raises(NeedRedirectToLogin):
        await check_auth(Tokens(None, token))


# @pytest.mark.asyncio
# async def test_ch
