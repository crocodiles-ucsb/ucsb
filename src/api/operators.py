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


@router.post('/')
async def add_operator(req: Request, operator_in: OperatorIn):
    return await AdminsController.add_operator(req, operator_in)


@router.get('/')
async def get_operator(req: Request):
    return await OperatorsController.get_operator_page(req)
