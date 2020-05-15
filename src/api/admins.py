from fastapi import APIRouter
from fastapi.requests import Request
from src.controller.admins import AdminsController
from src.models import OutUser
from starlette.templating import _TemplateResponse

router = APIRouter()


@router.get('/{admin_id}/add_operator')
async def get_add_operator_form(admin_id: int, req: Request):
    return await AdminsController.add_operator_form(req, admin_id)


@router.get('/{admin_id}/add_security')
async def get_add_security_form(admin_id: int, req: Request):
    return await AdminsController.add_security_form(req, admin_id)


@router.get('/{admin_id}')
async def get_admin(admin_id: int, req: Request) -> _TemplateResponse:
    return await AdminsController.get_admin_page(req, admin_id)


@router.get('/{admin_id}/securities')
async def get_admin(admin_id: int, req: Request) -> _TemplateResponse:
    return await AdminsController.get_securities_page(req, admin_id)


@router.post('')
async def add_admin(username: str, password: str) -> OutUser:
    return await AdminsController.add(username, password)
