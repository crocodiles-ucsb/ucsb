from src.DAL.securities import SecuritiesDAL
from src.api.catalogs import CatalogType
from src.controller.authorization_decorators import auth_required
from src.DAL.catalogs_dal import CatalogsDAL
from src.DAL.contractors_dal import ContractorsDAL
from src.DAL.representatives_dal import RepresentativesDAL
from src.DAL.requests import RequestsDAL
from src.DAL.tokens import get_user
from src.DAL.users.contractor_representative import ContractorRepresentativeAddingParams
from src.database.models import RequestStatus
from src.database.user_roles import UserRole
from src.models import RequestForTemplateOut
from src.templates import templates
from src.urls import Urls
from starlette.requests import Request
from starlette.responses import RedirectResponse


class RepresentativesController:
    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_request_result(
        req: Request, request_id: int, substring: str, page: int, size: int
    ):
        workers_with_pagination = await RequestsDAL.get_representative_request_result(
            request_id, (await get_user(req)).id, substring, page, size
        )
        request = await RequestsDAL.get_representative_request(request_id)
        return templates.TemplateResponse(
            'representative_request_result.html',
            {
                'base_url': Urls.base_url.value,
                'request': req,
                'request_': request,
                'workers': workers_with_pagination.data,
                'pagination': workers_with_pagination.pagination_params,
                'substring': substring,
            },
        )

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
        violations = await SecuritiesDAL.get_worker_violations(worker_id)
        worker = await RepresentativesDAL.get_worker(
            (await get_user(req)).id, worker_id
        )
        objects = await RepresentativesDAL.get_worker_objects(worker_id)
        return templates.TemplateResponse(
            'representatives_worker.html',
            {
                'request': req,
                'worker': worker,
                'base_url': Urls.base_url.value,
                'objects': objects,
                'violations' : violations
            },
        )

    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_add_worker_form(req: Request):
        professions = await CatalogsDAL.get_simple_catalog_items_without_pagination(
            CatalogType.professions
        )
        return templates.TemplateResponse(
            'worker_add_form.html', {'request': req, 'professions': professions}
        )

    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_add_request_form(req: Request):
        contracts = await ContractorsDAL.get_contracts((await get_user(req)).id)
        objects_of_work = await CatalogsDAL.get_simple_catalog_items_without_pagination(
            CatalogType.objects_of_work
        )
        return templates.TemplateResponse(
            'request_add_form.html',
            {
                'request': req,
                'base_url': Urls.base_url.value,
                'contracts': contracts,
                'objects_of_work': objects_of_work,
            },
        )

    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_closed_request_page(
        req: Request, request_id: int, substring: str, page: int, size: int
    ):
        pass

    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_request_page(
        req: Request, request_id: int, substring: str, page: int, size: int
    ):
        workers = await RequestsDAL.get_representative_workers_in_request(
            (await get_user(req)).id, request_id, substring, page, size
        )
        request = await RequestsDAL.get_representative_request(request_id)

        return templates.TemplateResponse(
            'representative_request_main.html',
            {
                'request': req,
                'workers': workers.data,
                'pagination': workers.pagination_params,
                'substring': substring,
                'request_id': request_id,
                'request_': request,
            },
        )

    @staticmethod
    @auth_required(UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False)
    async def get_filled_request_page(
        req: Request, request_id: int, substring: str, page: int, size: int
    ):
        request: RequestForTemplateOut = await RequestsDAL.get_representative_request(
            request_id
        )
        workers_with_pagination = await RequestsDAL.get_worker_from_requests(
            (await get_user(req)).id, request_id, substring, page, size
        )
        if request.status == RequestStatus.WAITING_FOR_VERIFICATION:
            template = 'representative_request_open.html'
        else:
            template = 'representative_request_closed.html'
        return templates.TemplateResponse(
            template,
            {
                'request': req,
                'workers': workers_with_pagination.data,
                'pagination': workers_with_pagination.pagination_params,
                'substring': substring,
                'request_id': request_id,
                'request_': request,
            },
        )
