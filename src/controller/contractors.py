from typing import Optional

from fastapi import UploadFile
from src.controller.authorization_decorators import auth_required
from src.DAL.contractors_dal import ContractorsDAL
from src.DAL.documents_dal import DocumentsDAL
from src.database.user_roles import UserRole
from src.models import DocumentWithTitleOut
from src.templates import templates
from starlette.requests import Request


class ContractorsController:
    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_contractors(req, page, size: int, substring: Optional[str]):
        contractors_list_with_pagination = await ContractorsDAL.get_all(
            substring, size, page
        )
        return templates.TemplateResponse(
            'operator-contractors.html',
            {
                'request': req,
                'contractors': contractors_list_with_pagination.data,
                'pagination': contractors_list_with_pagination.pagination_params,
                'substring': substring,
            },
        )

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def add_contractor(
        req: Request, title: str, address: str, ogrn: str, inn: str, **kwargs
    ):
        return await ContractorsDAL.add(title, address, ogrn, inn, **kwargs)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def add_contract(
        req: Request, contractor_id: int, title: str, file: UploadFile
    ) -> DocumentWithTitleOut:
        return await DocumentsDAL.add_contract(contractor_id, title, file)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False)
    async def get_contractor(req: Request, contracotr_id: int):
        return await ContractorsDAL.get(req, contracotr_id)
