from http import HTTPStatus

from fastapi import APIRouter
from src.controller.representatives import RepresentativesController
from src.DAL.users.contractor_representative import ContractorRepresentativeAddingParams
from starlette.requests import Request

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED.value)
async def add(req: Request, params: ContractorRepresentativeAddingParams):
    return await RepresentativesController.add(req, params)


@router.get('/workers')
async def get_workers_page(
    req: Request, substring: str = '', page: int = 1, size: int = 10
):
    return await RepresentativesController.get_workers_page(req, substring, page, size)


@router.get('/requests')
async def get_requests(
    req: Request,
    solved: bool = False,
    substring: str = '',
    page: int = 1,
    size: int = 10,
):
    return await RepresentativesController.get_requests_page(
        req, solved, substring, page, size
    )


@router.get('/workers/{worker_id}')
async def get_worker(req: Request, worker_id: int):
    return await RepresentativesController.get_worker_page(req, worker_id)


@router.get('/')
async def get_main_page(req: Request):
    return await RepresentativesController.get_main_page(req)
