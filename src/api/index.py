from http import HTTPStatus

from fastapi import APIRouter, Request
from src.controller.admins import AdminsController
from src.controller.index import IndexController
from src.models import InUserWithUUID

router = APIRouter()


@router.get('/')
async def get_index(req: Request):
    '''
    пустой html c логикой
    '''
    return await IndexController.transfer(req)


@router.get('/forbidden')
async def get_forbidden_page(req: Request):
    return IndexController.forbidden(req)


@router.get('/login')
async def login(req: Request):
    return await IndexController.get_login_page(req)


@router.get('/refresh_tokens')
async def refresh_tokens(req: Request, access_token: str, refresh_token: str):
    return IndexController.refresh_tokens(req, access_token, refresh_token)


@router.get('/register/{uuid}')
async def get_register_form(req: Request, uuid: str):
    return await IndexController.get_register_form(req, uuid)


@router.post('/users', status_code=HTTPStatus.CREATED.value)
async def add_user(user: InUserWithUUID):
    return await IndexController.register_user(user)


@router.delete('/users/{uuid}', status_code=HTTPStatus.NO_CONTENT.value)
async def remove_user(req: Request, uuid: str):
    return await AdminsController.remove_user(req, uuid)


@router.get('/logout')
async def logout(req: Request):
    return await IndexController.logout(req)
