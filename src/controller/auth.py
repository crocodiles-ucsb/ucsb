from typing import Optional

from src.controller.grant_type import GrantType
from src.DAL.auth import authorize
from src.models import TokensResponse


class AuthController:
    @staticmethod
    async def authorize_user(
        username: Optional[str],
        password: Optional[str],
        grant_type: GrantType,
        refresh_token: Optional[str],
    ) -> TokensResponse:
        return await authorize(grant_type, username, password, refresh_token)
