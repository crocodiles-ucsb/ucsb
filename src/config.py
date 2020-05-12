from pydantic import BaseSettings


class TokensSettings(BaseSettings):
    access_token_expire_minutes = 1
    refresh_toke_expire_time_days = 7
    token_type = 'bearer'


class ServiceSettings(BaseSettings):
    base_address = 'localhost'
    port = 8000
    base_url = f'http://{base_address}:{port}'
    login_url = f'{base_url}/login'
    refresh_token_url = f'{base_url}/refresh_tokens'
    forbidden_url = f'{base_url}/forbidden'
    registration_url = f'{base_url}/register'


tokens_settings = TokensSettings()
service_settings = ServiceSettings()
