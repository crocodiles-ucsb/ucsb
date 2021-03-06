from src.controller.authorization_decorators import auth_handler
from src.DAL import tokens
from src.DAL.registration import RegistrationViaUniqueLink, UniqueLinkRegistrationParams
from src.DAL.tokens import get_tokens
from src.models import InUserWithUUID, OutUser
from src.templates import templates
from src.urls import Urls
from starlette.requests import Request
from starlette.templating import _TemplateResponse


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
                {'request': req, 'base_url': Urls.base_url.value, 'uuid': uuid},
            )
        return 'Ссылка недействительна или ей уже кто-то воспользовался'

    @staticmethod
    async def get_login_page(req: Request):
        value = Urls.base_url.value
        return templates.TemplateResponse(
            'login.html', {'request': req, 'base_url': value}
        )

    @staticmethod
    async def register_user(in_user: InUserWithUUID) -> OutUser:
        return await RegistrationViaUniqueLink().register(
            UniqueLinkRegistrationParams(
                username=in_user.username, password=in_user.password, uuid=in_user.uuid
            )
        )

    @staticmethod
    async def logout(req: Request) -> _TemplateResponse:
        return templates.TemplateResponse(
            'logout.html', {'request': req, 'base_url': Urls.base_url.value}
        )
