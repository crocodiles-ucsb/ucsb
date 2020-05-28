from src.controller.authorization_decorators import auth_required
from src.DAL.requests import RequestsDAL
from src.DAL.tokens import get_user
from src.database.user_roles import UserRole
from src.models import RequestIn, RequestOut, WorkerInRequestIn, WorkerInRequestOut
from starlette.requests import Request


class RequestsController:
    @staticmethod
    @auth_required(
        UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False, auth_redirect=False
    )
    async def add(req: Request, params: RequestIn) -> RequestOut:
        return await RequestsDAL.add(await get_user(req), params)

    @staticmethod
    @auth_required(
        UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False, auth_redirect=False
    )
    async def add_worker(
        req: Request, request_id: int, params: WorkerInRequestIn
    ) -> WorkerInRequestOut:
        return await RequestsDAL.add_worker_to_request(
            await get_user(req), request_id, params.worker_id
        )

    @staticmethod
    @auth_required(
        UserRole.CONTRACTOR_REPRESENTATIVE, check_id=False, auth_redirect=False
    )
    async def delete_worker_from_request(
        req: Request, request_id: int, worker_id: int
    ) -> None:
        return await RequestsDAL.delete_worker_from_request(
            await get_user(req), request_id, worker_id
        )
