from fastapi import APIRouter

from src.database.database import create_session
from src.database.models import User

router = APIRouter()


@router.post('')
async def add_admin():
    with create_session() as session:

