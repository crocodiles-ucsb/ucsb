from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from src.DAL.auth import check_authorization
from src.DAL.utils import get_url_postfix

from src.templates import templates

router = APIRouter()
from src.config import service_settings

@router.get('/')
async def get_index(req: Request):
    '''
    пустой html c логикой
    '''
    token = req.cookies.get('access_token')
    if token:
        user = await check_authorization(token)
        return RedirectResponse(f'{service_settings.base_url}{get_url_postfix(user)}')
    return RedirectResponse(service_settings.login_url)


@router.get('/login')
async def login(req: Request):
    '''
    авторизация с логикой
    '''
    return templates.TemplateResponse('login.html', {'request': req})
