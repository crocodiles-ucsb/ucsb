from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter
from fastapi.requests import Request
from src.api.catalogs import CatalogType
from src.controller.admins import AdminsController
from src.models import OutUser
from starlette.templating import _TemplateResponse

router = APIRouter()


@router.get('/{admin_id}/add_operator')
async def get_add_operator_form(req: Request, admin_id: int):
    return await AdminsController.add_operator_form(req, admin_id)


@router.get('/{admin_id}/add_security')
async def get_add_security_form(admin_id: int, req: Request):
    return await AdminsController.add_security_form(req, admin_id)


@router.get('/{admin_id}')
async def get_admin(req: Request, admin_id: int) -> _TemplateResponse:
    return await AdminsController.get_admin_page(req, admin_id)


@router.get('/{admin_id}/operators')
async def get_operators(
    admin_id: int,
    req: Request,
    page: int = 1,
    pending: bool = False,
    substring: Optional[str] = None,
) -> _TemplateResponse:
    return await AdminsController.get_operators(req, admin_id, page, pending, substring)


@router.get('/{admin_id}/securities')
async def get_securities(
    admin_id: int,
    req: Request,
    page: int = 1,
    pending: bool = False,
    substring: Optional[str] = None,
) -> _TemplateResponse:
    return await AdminsController.get_securities(
        req, admin_id, page, pending, substring
    )


@router.get('/{admin_id}/catalogs')
async def get_catalogs(req: Request, admin_id: int):
    return await AdminsController.get_catalogs(req, admin_id)


@router.get('/{admin_id}/catalogs/{catalog_type}')
async def get_catalog(
    req: Request,
    admin_id: int,
    catalog_type: CatalogType,
    page: int = 1,
    substring: Optional[str] = None,
):
    return await AdminsController.get_catalog(
        req, admin_id, catalog_type, page, substring
    )


@router.post('/{admin_id}/catalogs/{catalog_type}')
async def add_catalog(
    admin_id: int,
    req: Request,
    catalog_type: CatalogType,
    data: str,
    value: Optional[int] = None,
):
    return await AdminsController.add_catalog_data(
        req, admin_id, catalog_type, data, value, catalog_type.out_model
    )


@router.delete('/catalogs/{catalog_id}', status_code=HTTPStatus.NO_CONTENT.value)
async def delete_catalog_item(req: Request, catalog_id: int):
    return await AdminsController.delete_catalog(req, catalog_id)


@router.post('')
async def add_admin(username: str, password: str) -> OutUser:
    return await AdminsController.add(username, password)
