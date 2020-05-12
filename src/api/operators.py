from http import HTTPStatus

from fastapi import APIRouter, Form
from starlette.responses import RedirectResponse

from src.controller.admins import AdminsController
from starlette.requests import Request
from src.models import OperatorToRegisterOut, OperatorIn
from src.config import service_settings
router = APIRouter()


@router.post('/')
async def add_operator(
        req: Request,
        operator_in: OperatorIn
):
    return await AdminsController.add_operator(
        req, operator_in)

