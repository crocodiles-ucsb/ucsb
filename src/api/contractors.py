from http import HTTPStatus

from fastapi import APIRouter, File, Form, UploadFile
from src.controller.contractors import ContractorsController
from starlette.requests import Request
from starlette.templating import _TemplateResponse

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


@router.get('/{contractor_id}/add_contract')
async def add_contract(req: Request, contractor_id: int):
    return await ContractorsController.get_add_contract_form(req, contractor_id)


@router.post('/{contractor_id}/documents', status_code=HTTPStatus.CREATED.value)
async def add_document(
    request: Request,
    contractor_id: int,
    title: str = Form(...),
    file: UploadFile = File(...),
):
    return await ContractorsController.add_contract(request, contractor_id, title, file)


@router.get('/{contractor_id}')
async def get_contractor(
    req: Request, contractor_id: int, substring: str = '', page: int = 1, size: int = 10
) -> _TemplateResponse:
    return await ContractorsController.get_contractor(
        req, contractor_id, substring, page, size
    )
