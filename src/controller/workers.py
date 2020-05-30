from datetime import date

from src.controller.authorization_decorators import auth_required
from src.DAL.representatives_dal import RepresentativesDAL
from src.DAL.tokens import get_user
from src.database.user_roles import UserRole
from src.models import WorkerWithProfessionOut
from starlette.requests import Request


class WorkersController:
    @staticmethod
    @auth_required(
        UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False, auth_redirect=False
    )
    async def add(
        req: Request,
        last_name: str,
        first_name: str,
        patronymic: str,
        birthday: date,
        profession: str,
        **kwargs
    ) -> WorkerWithProfessionOut:
        contractor_representative = await get_user(req)
        return await RepresentativesDAL.add_worker(
            contractor_representative,
            last_name,
            first_name,
            patronymic,
            birthday,
            profession,
            **kwargs
        )
