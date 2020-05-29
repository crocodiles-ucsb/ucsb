from http import HTTPStatus

from fastapi import APIRouter
from src.controller.requests import RequestsController
from src.models import RequestIn, RequestOut, WorkerInRequestIn, WorkerInRequestOut
from starlette.requests import Request

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED.value)
async def add_request(req: Request, request: RequestIn) -> RequestOut:
    return await RequestsController.add(req, request)


@router.post('{request_id}/workers', status_code=HTTPStatus.CREATED.value)
async def add_worker_to_request(
    req: Request, request_id: int, params: WorkerInRequestIn
) -> WorkerInRequestOut:
    return await RequestsController.add_worker(req, request_id, params)


@router.delete(
    '/{request_id}/workers/{worker_id}', status_code=HTTPStatus.NO_CONTENT.value
)
async def delete_worker_from_request(
    req: Request, request_id: int, worker_id: int
) -> None:
    return await RequestsController.delete_worker_from_request(
        req, request_id, worker_id
    )


@router.post('{request_id}/send_request')
async def send_request(req: Request, request_id: int) -> RequestOut:
    return await RequestsController.send_request(req, request_id)
