from http import HTTPStatus

from fastapi import APIRouter
from src.controller.representatives import RepresentativesController
from src.DAL.users.contractor_representative import ContractorRepresentativeAddingParams
from starlette.requests import Request

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED.value)
async def add(req: Request, params: ContractorRepresentativeAddingParams):
    return await RepresentativesController.add(req, params)


@router.get('/add_worker')
async def add_worker_page(req: Request):
    return await RepresentativesController.get_add_worker_form(req)


@router.get('/add_request')
async def add_worker_page(req: Request):
    return await RepresentativesController.get_add_request_form(req)


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


@router.get('/filled_requests/{request_id}')
async def get_get_closed_request(
    req: Request, request_id: int, substring: str = '', page: int = 1, size: int = 10
):
    return await RepresentativesController.get_filled_request_page(req, request_id, substring, page, size)


@router.get('/requests/{request_id}/result')
async def get_result_of_request(
    req: Request, request_id: int, substring: str = '', page: int = 1, size: int = 10
):
    return await RepresentativesController.get_request_result(
        req, request_id, substring, page, size
    )


@router.get('/requests/{request_id}')
async def get_request(
    req: Request, request_id: int, substring: str = '', page: int = 1, size: int = 10
):
    return await RepresentativesController.get_request_page(
        req, request_id, substring, page, size
    )


@router.get('/workers/{worker_id}')
async def get_worker(req: Request, worker_id: int):
    return await RepresentativesController.get_worker_page(req, worker_id)


@router.get('/')
async def get_main_page(req: Request):
    return await RepresentativesController.get_main_page(req)
