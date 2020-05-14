from fastapi import APIRouter
from src.controller.admins import AdminsController
from src.models import OperatorIn
from starlette.requests import Request

router = APIRouter()


@router.post('/')
async def add_operator(req: Request, operator_in: OperatorIn):
    return await AdminsController.add_operator(req, operator_in)
