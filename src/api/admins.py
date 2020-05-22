from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter
from fastapi.requests import Request
from src.api.catalogs import CatalogType
from src.controller.admins import AdminsController
from src.models import OutUser
from starlette.templating import _TemplateResponse

router = APIRouter()


@router.get('/catalogs')
async def get_catalogs(req: Request):
    return await AdminsController.get_catalogs(req)


@router.get('/catalogs/{catalog_type}')
async def get_catalog(
        req: Request,
        catalog_type: CatalogType,
        page: int = 1,
        substring: Optional[str] = None,
):
    return await AdminsController.get_catalog(
        req, catalog_type, page, substring
    )


@router.get('/add_catalog/{catalog_type}')
async def get_add_catalog_page(req: Request, catalog_type: CatalogType):
    return await AdminsController.get_add_catalog_page(req, catalog_type)


@router.post('/catalogs/{catalog_type}', status_code=HTTPStatus.CREATED.value)
async def add_catalog(
        req: Request,
        catalog_type: CatalogType,
        data: str,
        value: Optional[int] = None,
):
    return await AdminsController.add_catalog_data(
        req, catalog_type, data, value, catalog_type.out_model
    )


@router.delete('/catalogs/{catalog_id}', status_code=HTTPStatus.NO_CONTENT.value)
async def delete_catalog_item(req: Request, catalog_id: int):
    return await AdminsController.delete_catalog(req, catalog_id)


@router.get('/add_operator')
async def get_add_operator_form(req: Request):
    return await AdminsController.add_operator_form(req)


@router.get('/add_security')
async def get_add_security_form(req: Request):
    return await AdminsController.add_security_form(req)


@router.get('/securities')
async def get_securities(
        req: Request,
        page: int = 1,
        pending: bool = False,
        substring: Optional[str] = None,
) -> _TemplateResponse:
    return await AdminsController.get_securities(
        req, page, pending, substring
    )


@router.get('/operators')
async def get_operators(
        req: Request,
        page: int = 1,
        pending: bool = False,
        substring: Optional[str] = None,
) -> _TemplateResponse:
    return await AdminsController.get_operators(req, page, pending, substring)


@router.get('/{admin_id}')
async def get_admin(req: Request, admin_id: int) -> _TemplateResponse:
    return await AdminsController.get_admin_page(req)


@router.post('')
async def add_admin(username: str, password: str) -> OutUser:
    return await AdminsController.add(username, password)


@router.get('')
async def get_admin_page(req: Request):
    return await AdminsController.get_admin_page(req)
