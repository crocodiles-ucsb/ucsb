from typing import Optional

from fastapi import APIRouter
from src.DAL.auth import authorize
from src.DAL.grant_type import GrantType
from src.models import TokensResponse

router = APIRouter()


@router.post('/auth', response_model=TokensResponse)
async def authorize_user(
    grant_type: GrantType,
    username: Optional[str] = None,
    password: Optional[str] = None,
    refresh_token: Optional[str] = None,
) -> TokensResponse:
    return await authorize(grant_type, username, password, refresh_token)
