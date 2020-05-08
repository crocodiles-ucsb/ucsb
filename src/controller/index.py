from src.DAL import tokens
from src.DAL.utils import auth_handler, get_tokens
from src.templates import templates
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
            },
        )

    @staticmethod
    def forbidden(req: Request) -> _TemplateResponse:
        return templates.TemplateResponse('forbidden.html', {'request': req})
