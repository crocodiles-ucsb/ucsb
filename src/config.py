from pydantic import BaseSettings


class TokensSettings(BaseSettings):
    access_token_expire_minutes = 15
    refresh_toke_expire_time_days = 7
    token_type = 'bearer'


class ServiceSettings(BaseSettings):
    base_address = '185.189.14.105'
    port = 80
    base_url = f'http://{base_address}:{port}'
    login_url = f'{base_url}/login'


tokens_settings = TokensSettings()
service_settings = ServiceSettings()
