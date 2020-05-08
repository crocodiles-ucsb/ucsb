from fastapi import APIRouter
from fastapi.requests import Request
from src.controller.admins import AdminsController
from src.models import OutUser
from starlette.templating import _TemplateResponse

router = APIRouter()


@router.get('/{admin_id}')
async def get_admin(admin_id: int, req: Request) -> _TemplateResponse:
    return await AdminsController.get_admin_page(admin_id, req)


@router.post('')
async def add_admin(username: str, password: str) -> OutUser:
    return await AdminsController.add(username, password)
