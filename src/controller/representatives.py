from src.controller.authorization_decorators import auth_required
from src.DAL.representatives_dal import RepresentativesDAL
from src.DAL.requests import RequestsDAL
from src.DAL.tokens import get_user
from src.DAL.users.contractor_representative import ContractorRepresentativeAddingParams
from src.database.user_roles import UserRole
from src.templates import templates
from src.urls import Urls
from starlette.requests import Request
from starlette.responses import RedirectResponse


class RepresentativesController:
    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def add(req: Request, params: ContractorRepresentativeAddingParams):
        return await RepresentativesDAL.add(params)

    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_main_page(req: Request):
        return RedirectResponse(
            f'{Urls.base_url.value}/contractor_representatives/workers',
        )

    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_workers_page(req: Request, substring: str, page: int, size: int):
        workers_with_pagination = await RequestsDAL.get_representative_workers(
            (await get_user(req)).id, substring=substring, page=page, size=size
        )
        return templates.TemplateResponse(
            'representatives_workers.html',
            {
                'request': req,
                'workers': workers_with_pagination.data,
                'pagination': workers_with_pagination.pagination_params,
                'substring': substring,
            },
        )

    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_requests_page(
            req: Request, solved: bool, substring: str, page: int, size: int
    ):
        requests_with_pagination = await RequestsDAL.get_representative_requests(
            (await get_user(req)).id, substring, page, size, solved
        )
        template = (
            'representatives_closed_requests.html'
            if solved
            else 'representatives_requests.html'
        )
        return templates.TemplateResponse(
            template,
            {
                'request': req,
                'pagination': requests_with_pagination.pagination_params,
                'requests': requests_with_pagination.data,
                'substring': substring,
            },
        )

    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_worker_page(req: Request, worker_id: int):
        worker = await RepresentativesDAL.get_worker(
            (await get_user(req)).id, worker_id
        )
        return templates.TemplateResponse(
            'representatives_worker.html', {'request': req, 'worker': worker, 'base_url': Urls.base_url.value}
        )
