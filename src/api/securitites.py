from fastapi import APIRouter
from src.controller.admins import AdminsController
from src.controller.securities import SecuritiesController
from src.models import SecurityIn, PenaltyIn
from starlette.requests import Request

router = APIRouter()


@router.get('/workers/{worker_id}')
async def get_worker(req: Request, worker_id: int):
    return await SecuritiesController.get_worker(req, worker_id)


@router.get('/workers/{worker_id}/add_violation')
async def add_violation_page(req: Request, worker_id: int):
    return await SecuritiesController.add_violation_page(req, worker_id)


@router.post('/workers/{worker_id}/penalties')
async def add_penalty(req: Request, worker_id: int, params: PenaltyIn):
    await SecuritiesController.add_penalty(req, worker_id, params)


@router.get('/workers')
async def get_workers(req: Request, substring: str = '', page: int = 1, size: int = 10):
    return await SecuritiesController.get_workers(req, substring, page, size)


@router.post('/')
async def add_securities(req: Request, in_security: SecurityIn):
    return await AdminsController.add_security(req, in_security)


@router.get('/')
async def get_security_page(req: Request):
    return await SecuritiesController.get_page(req)
