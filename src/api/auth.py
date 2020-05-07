from typing import Optional

from fastapi import APIRouter, Form
from src.controller.auth import AuthController
from src.controller.grant_type import GrantType
from src.models import TokensResponse

router = APIRouter()


@router.post('/auth', response_model=TokensResponse)
async def authorize_user(
    grant_type: GrantType = Form(...),
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    refresh_token: Optional[str] = Form(None),
) -> TokensResponse:
    return await AuthController.authorize_user(
        username=username,
        password=password,
        grant_type=grant_type,
        refresh_token=refresh_token,
    )
