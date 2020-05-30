from fastapi import APIRouter
from src.controller.admins import AdminsController
from src.controller.operator import OperatorsController
from src.models import OperatorIn
from starlette.requests import Request
from starlette.responses import HTMLResponse

router = APIRouter()


@router.get('/representative_add_form')
async def get_representative_add_form(req: Request, contractor_id: int) -> HTMLResponse:
    return await OperatorsController.get_representative_add_form(req, contractor_id)


@router.get('/contractor_add_form')
async def get_contractor_add_form(req: Request):
    return await OperatorsController.get_contractor_add_form(req)


@router.get('/requests')
async def get_requests(
    req: Request, substring: str = '', page: int = 1, size: int = 10
):
    return await OperatorsController.get_requests(req, substring, page, size)


@router.get('/requests/{request_id}')
async def get_request(
    req: Request, request_id: int, substring: str = '', page: int = 1, size: int = 10
):
    return await OperatorsController.get_request(req, request_id, substring, page, size)


@router.post('/')
async def add_operator(req: Request, operator_in: OperatorIn):
    return await AdminsController.add_operator(req, operator_in)


@router.get('/')
async def get_operator(req: Request):
    return await OperatorsController.get_operator_page(req)
