from functools import lru_cache

from pydantic import BaseSettings


class TokensSettings(BaseSettings):
    access_token_expire_minutes = 1
    refresh_toke_expire_time_days = 7
    token_type = 'bearer'


class ServiceSettings(BaseSettings):
    base_address = 'localhost'
    port = 8000


@lru_cache()
def _get_service_settings() -> ServiceSettings:
    return ServiceSettings()


@lru_cache()
def _get_tokens_settings() -> TokensSettings:
    return TokensSettings()


tokens_settings = _get_tokens_settings()
service_settings = _get_service_settings()
