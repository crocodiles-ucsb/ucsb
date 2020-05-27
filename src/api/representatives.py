from http import HTTPStatus

from fastapi import APIRouter
from src.controller.representatives import RepresentativesController
from src.DAL.users.contractor_representative import ContractorRepresentativeAddingParams
from starlette.requests import Request

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED.value)
async def add(req: Request, params: ContractorRepresentativeAddingParams):
    return await RepresentativesController.add(req, params)
