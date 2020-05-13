from enum import Enum

from src.config import service_settings


class Urls(Enum):
    base_url = f'http://{service_settings.base_address}:{service_settings.port}'
    login_url = f'{base_url}/login'
    refresh_token_url = f'{base_url}/refresh_tokens'
    forbidden_url = f'{base_url}/forbidden'
    registration_url = f'{base_url}/register'
