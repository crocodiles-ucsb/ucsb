from src.DAL.securities import SecuritiesDAL
from src.api.catalogs import CatalogType
from src.controller.authorization_decorators import auth_required
from src.DAL.catalogs_dal import CatalogsDAL
from src.DAL.requests import RequestsDAL
from src.DAL.tokens import get_user
from src.database.user_roles import UserRole
from src.models import (
    DenyWorkerIn,
    RequestIn,
    RequestOut,
    WorkerInRequestIn,
    WorkerInRequestOut,
)
from src.templates import templates
from src.urls import Urls
from starlette.requests import Request


class RequestsController:
    @staticmethod
    @auth_required(
        UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False, auth_redirect=False
    )
    async def add(req: Request, params: RequestIn) -> RequestOut:
        return await RequestsDAL.add(await get_user(req), params)

    @staticmethod
    @auth_required(
        UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False, auth_redirect=False
    )
    async def add_worker(
        req: Request, request_id: int, params: WorkerInRequestIn
    ) -> WorkerInRequestOut:
        return await RequestsDAL.add_worker_to_request(
            await get_user(req), request_id, params.worker_id
        )

    @staticmethod
    @auth_required(
        UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False, auth_redirect=False
    )
    async def delete_worker_from_request(
        req: Request, request_id: int, worker_id: int
    ) -> None:
        return await RequestsDAL.delete_worker_from_request(
            await get_user(req), request_id, worker_id
        )

    @staticmethod
    async def send_request(req: Request, request_id: int) -> RequestOut:
        return await RequestsDAL.send_request(await get_user(req), request_id)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def accept_worker(
        req: Request, request_id: int, worker_id: int
    ) -> WorkerInRequestOut:
        return await RequestsDAL.accept_worker(request_id, worker_id)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def deny_worker(
        req: Request, request_id: int, worker_id: int, params: DenyWorkerIn
    ):
        return await RequestsDAL.deny_worker(request_id, worker_id, params)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def deny_worker(
        req: Request, request_id: int, worker_id: int, params: DenyWorkerIn
    ):
        return await RequestsDAL.deny_worker(request_id, worker_id, params)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def close(req: Request, request_id: int) -> RequestOut:
        return await RequestsDAL.close(request_id)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def reset_worker_in_request(
        req: Request, request_id: int, worker_id: int
    ) -> WorkerInRequestOut:
        return await RequestsDAL.reset_worker_in_request_status(request_id, worker_id)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_deny_form(req, request_id, worker_id):
        reasons = await CatalogsDAL.get_simple_catalog_items_without_pagination(
            CatalogType.reasons_for_rejection_of_application
        )
        return templates.TemplateResponse(
            'request_denial_form.html',
            {
                'request': req,
                'base_url': Urls.base_url.value,
                'request_id': request_id,
                'worker_id': worker_id,
                'reasons': reasons,
            },
        )

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_worker(req: Request, request_id: int, worker_id: int):
        worker = await RequestsDAL.get_worker(request_id, worker_id)
        violations = await SecuritiesDAL.get_worker_violations(worker_id)
        return templates.TemplateResponse(
            'worker_in_request.html',
            {
                'request': req,
                'base_url': Urls.base_url.value,
                'worker': worker,
                'request_id': request_id,
                'violations': violations
            },
        )

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_request_result(
        req: Request, request_id: int, substring: str, page: int, size: int
    ):
        workers_with_pagination = await RequestsDAL.get_operator_workers_in_request(
            request_id, substring, page, size, is_result=True
        )
        request = await RequestsDAL.get_operator_request(request_id)
        return templates.TemplateResponse(
            'operator_requests_result.html',
            {
                'request': req,
                'workers': workers_with_pagination.data,
                'request_': request,
                'substring': substring,
                'pagination': workers_with_pagination.pagination_params,
            },
        )
