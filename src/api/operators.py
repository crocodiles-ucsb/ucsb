
from fastapi import APIRouter
from src.controller.admins import AdminsController
from src.controller.operator import OperatorsController
from src.models import OperatorIn
from starlette.requests import Request

router = APIRouter()


@router.get('/representative_add_form')
async def get_representative_add_form(req: Request):
    return await OperatorsController.get_representative_add_form(req)


@router.get('/contractor_add_form')
async def get_contractor_add_form(req: Request):
    return await OperatorsController.get_contractor_add_form(req)


@router.post('/representatives')
async def add_representative(req: Request):
    pass


@router.post('/')
async def add_operator(req: Request, operator_in: OperatorIn):
    return await AdminsController.add_operator(req, operator_in)


@router.get('/')
async def get_operator(req: Request):
    return await OperatorsController.get_operator_page(req)
