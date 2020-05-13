from src.controller.authorization_decorators import auth_handler
from src.DAL import tokens
from src.DAL.registration import RegistrationViaUniqueLink
from src.DAL.tokens import get_tokens
from src.templates import templates
from starlette.requests import Request
from starlette.templating import _TemplateResponse

from src.urls import Urls


class IndexController:
    @staticmethod
    @auth_handler
    async def transfer(req: Request) -> None:
        await tokens.check_auth(get_tokens(req))

    @staticmethod
    def refresh_tokens(
            req: Request, access_token: str, refresh_token: str
    ) -> _TemplateResponse:
        return templates.TemplateResponse(
            'refresh_tokens.html',
            {
                'request': req,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'base_url': Urls.base_url.value,
            },
        )

    @staticmethod
    def forbidden(req: Request) -> _TemplateResponse:
        return templates.TemplateResponse(
            'forbidden.html', {'request': req, 'base_url': Urls.base_url.value}
        )

    @staticmethod
    async def get_register_form(req: Request, uuid: str) -> _TemplateResponse:
        if await RegistrationViaUniqueLink.is_valid_uuid(uuid):
            return templates.TemplateResponse(
                'registration.html',
                {'request': req, 'base_url': Urls.base_url.value},
            )
        return 'Ссылка недействительна или устарела'

    @staticmethod
    async def get_login_page(req: Request):
        value = Urls.base_url.value
        print(value)
        return templates.TemplateResponse(
            'login.html', {'request': req, 'base_url': value}
        )
