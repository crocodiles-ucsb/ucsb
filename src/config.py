from functools import lru_cache

from pydantic import BaseSettings


class TokensSettings(BaseSettings):
    access_token_expire_minutes = 20
    refresh_toke_expire_time_days = 7
    token_type = 'bearer'


class ServiceSettings(BaseSettings):
    base_address = 'localhost'
    port = 8000


class StorageSettings(BaseSettings):
    main_directory_name: str = 'storage'


@lru_cache()
def _get_service_settings() -> ServiceSettings:
    return ServiceSettings()


@lru_cache()
def _get_tokens_settings() -> TokensSettings:
    return TokensSettings()


tokens_settings = _get_tokens_settings()
service_settings = _get_service_settings()
storage_settings = StorageSettings()
