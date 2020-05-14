from fastapi import APIRouter
from src.controller.admins import AdminsController
from src.controller.operator import OperatorsController
from src.models import OperatorIn
from starlette.requests import Request

router = APIRouter()


@router.post('/')
async def add_operator(req: Request, operator_in: OperatorIn):
    return await AdminsController.add_operator(req, operator_in)


@router.get('/{operator_id}')
async def get_operator_page(req: Request, operator_id: int):
    return await OperatorsController.get_operator_page(req, operator_id)
