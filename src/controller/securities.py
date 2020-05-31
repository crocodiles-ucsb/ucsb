from src.DAL.catalogs_dal import CatalogsDAL
from src.api.catalogs import CatalogType
from src.controller.authorization_decorators import auth_required
from src.DAL.securities import SecuritiesDAL
from src.DAL.utils import ListWithPagination
from src.database.user_roles import UserRole
from src.models import WorkerSimpleOut, PenaltyIn
from src.templates import templates
from src.urls import Urls
from starlette.requests import Request
from starlette.responses import RedirectResponse


class SecuritiesController:
    @staticmethod
    @auth_required(UserRole.SECURITY, check_id=False)
    async def get_page(req: Request) -> RedirectResponse:
        return RedirectResponse(f'{Urls.base_url.value}/securities/workers')

    @staticmethod
    @auth_required(UserRole.SECURITY, check_id=False)
    async def get_worker(req: Request, worker_id: int):
        violations = await SecuritiesDAL.get_worker_violations(worker_id)
        worker = await SecuritiesDAL.get_worker(worker_id)
        return templates.TemplateResponse('security_worker.html', {'request': req, 'worker': worker, 'violations':
            violations, 'base_url': Urls.base_url.value})

    @staticmethod
    @auth_required(UserRole.SECURITY, check_id=False)
    async def get_workers(
            req: Request, substring: str, page: int, size: int
    ) -> ListWithPagination[WorkerSimpleOut]:
        workers_with_pagination = await SecuritiesDAL.get_workers(substring, page, size)
        return templates.TemplateResponse(
            'security_workers.html',
            {
                'request': req,
                'base_url': Urls.base_url.value,
                'workers': workers_with_pagination.data,
                'pagination': workers_with_pagination.pagination_params,
                'substring': substring,
            },
        )

    @staticmethod
    @auth_required(UserRole.SECURITY, check_id=False)
    async def add_violation_page(req: Request, worker_id: int):
        violations = await CatalogsDAL.get_simple_catalog_items_without_pagination(CatalogType.violations)
        objects = await CatalogsDAL.get_simple_catalog_items_without_pagination(CatalogType.objects_of_work)
        return templates.TemplateResponse('violation_add_form.html', {'request': req, 'base_url': Urls.base_url.value,
                                                                      'violations': violations, 'objects': objects,
                                                                      'worker_id': worker_id})

    @staticmethod
    @auth_required(UserRole.SECURITY, check_id=False)
    async def add_penalty(req: Request, worker_id: int, params: PenaltyIn):
        await SecuritiesDAL.add_penalty(worker_id, params)
