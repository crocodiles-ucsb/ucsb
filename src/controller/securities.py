from src.controller.authorization_decorators import auth_required
from src.database.user_roles import UserRole
from src.templates import templates
from starlette.requests import Request
from starlette.templating import _TemplateResponse


class SecuritiesController:
    @staticmethod
    @auth_required(UserRole.SECURITY)
    async def get_page(req: Request, security_id: int) -> _TemplateResponse:
        return templates.TemplateResponse('security.html', {'request': req})
