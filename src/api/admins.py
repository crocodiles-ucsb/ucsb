from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from src.DAL.auth import check_authorization
from src.database.database import create_session
from src.database.models import User, Admin
from src.models import OutUser

router = APIRouter()
from src.password import get_password_hash


@router.get('/{admin_id}')
async def get_admin(admin_id: int, user: OutUser = Depends(check_authorization)):
    '''
    возвращает страничку админа
    :param admin_id:
    :return:
    '''
    return 'admin page'


@router.post('')
async def add_admin(username: str, password: str):
    with create_session() as session:
        admin = Admin(username=username, password_hash=get_password_hash(password))
        session.add(admin)
