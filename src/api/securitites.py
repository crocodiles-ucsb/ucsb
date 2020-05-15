from fastapi import APIRouter
from src.controller.admins import AdminsController
from src.controller.securities import SecuritiesController
from src.models import SecurityIn
from starlette.requests import Request

router = APIRouter()


@router.post('/')
async def add_securities(req: Request, in_security: SecurityIn):
    return await AdminsController.add_security(req, in_security)


@router.get('/{security_id}')
async def get_security_page(req: Request, security_id: int):
    return await SecuritiesController.get_page(req, security_id)
