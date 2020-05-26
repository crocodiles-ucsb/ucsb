from http import HTTPStatus

from fastapi import APIRouter, File, Form, UploadFile
from src.controller.contractors import ContractorsController
from starlette.requests import Request

router = APIRouter()


@router.get('/')
async def get_contractors(
    req: Request, substring: str = '', page: int = 1, size: int = 10
):
    return await ContractorsController.get_contractors(req, page, size, substring)


@router.post('/', status_code=HTTPStatus.CREATED.value)
async def contractors(
    req: Request,
    title: str = Form(...),
    address: str = Form(...),
    ogrn: str = Form(...),
    inn: str = Form(...),
    ogrn_document: UploadFile = File(...),
    inn_document: UploadFile = File(...),
):
    return await ContractorsController.add_contractor(
        req,
        title,
        address,
        ogrn,
        inn,
        ogrn_document=ogrn_document,
        inn_document=inn_document,
    )
