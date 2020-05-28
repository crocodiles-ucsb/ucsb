from src.controller.authorization_decorators import auth_required
from src.DAL.representatives_dal import RepresentativesDAL
from src.DAL.users.contractor_representative import ContractorRepresentativeAddingParams
from src.database.user_roles import UserRole
from starlette.requests import Request


class RepresentativesController:
    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def add(req: Request, params: ContractorRepresentativeAddingParams):
        return await RepresentativesDAL.add(params)
