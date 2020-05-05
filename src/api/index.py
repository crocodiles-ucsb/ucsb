from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from starlette.templating import Jinja2Templates

from src.DAL.auth import check_authorization
from src.models import OutUser, MyModel

router = APIRouter()

templates = Jinja2Templates(directory='src/templates')


@router.get('/')
async def get_index(req: Request):
    '''
    пустой html c логикой
    '''
    return templates.TemplateResponse('index.html', {'request': req})


@router.get('/role', response_model=MyModel)
async def get_role(req: Request, user: OutUser = Depends(check_authorization)):
    '''
    берет инфу из хедера и возвращает url
    '''
    return RedirectResponse('http://loaclhost:8000/' + f'{user.type}s/{user.id}', headers=req.headers)
    # print(user)
    # return MyModel(url=f'{user.type}s/{user.id}')


@router.get('/login')
async def login(req: Request):
    '''
    авторизация с логикой
    '''
    return templates.TemplateResponse('auth.html', {'request': req})
