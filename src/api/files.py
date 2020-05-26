from fastapi import APIRouter
from src.controller.files import FilesController

router = APIRouter()


@router.get('/{file_id}')
async def get_file(file_id: str):
    return await FilesController.get_file(file_id)
