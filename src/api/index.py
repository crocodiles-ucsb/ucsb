from fastapi import APIRouter, Request
from src.controller.index import IndexController
from src.DAL.auth import refresh_tokens
from src.templates import templates

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
    return templates.TemplateResponse('login.html', {'request': req})


@router.get('/refresh_tokens')
async def refresh_tokens(req: Request, access_token: str, refresh_token: str):
    return IndexController.refresh_tokens(req, access_token, refresh_token)
