from typing import Optional

from pydantic import BaseModel
from src.controller.authorization_decorators import auth_required
from src.DAL.requests import RequestsDAL
from src.database.user_roles import UserRole
from src.templates import templates
from src.urls import Urls
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse


class OperatorOut(BaseModel):
    username: str
    first_name: str
    last_name: str
    patronymic: Optional[str]
    password_hash: str

    class Config:
        orm_mode = True


class OperatorsController:
    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_requests(
        req: Request, substring: str, page: int, size: int
    ) -> _TemplateResponse:
        requests_with_pagination = await RequestsDAL.get_operators_requests(
            substring, page, size
        )
        return templates.TemplateResponse(
            'operator-requests.html',
            {
                'request': req,
                'requests': requests_with_pagination.data,
                'pagination': requests_with_pagination.pagination_params,
                'base_url': Urls.base_url.value,
                'substring': substring,
            },
        )

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_operator_page(request: Request):
        return RedirectResponse(f'{Urls.base_url.value}/contractors')

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_representative_add_form(
        req: Request, contractor_id: int
    ) -> _TemplateResponse:
        return templates.TemplateResponse(
            'operator-representative-add-form.html',
            {
                'request': req,
                'contractor_id': contractor_id,
                'base_url': Urls.base_url.value,
            },
        )

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_contractor_add_form(req) -> _TemplateResponse:
        return templates.TemplateResponse(
            'operator-contractor-add-form.html',
            {'request': req, 'base_url': Urls.base_url.value},
        )

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_request(
        req: Request, request_id: int, substring: str, page: int, size: int
    ) -> _TemplateResponse:
        request = await RequestsDAL.get_operator_request(request_id)
        workers_with_pagination = await RequestsDAL.get_operator_workers_in_request(
            request_id, substring, page, size
        )
        return templates.TemplateResponse(
            'operator-request.html',
            {
                'request': req,
                'base_url': Urls.base_url.value,
                'request_': request,
                'workers': workers_with_pagination.data,
                'pagination': workers_with_pagination.pagination_params,
                'substring': substring,
            },
        )
