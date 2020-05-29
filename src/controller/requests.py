
from src.controller.authorization_decorators import auth_required
from src.DAL.requests import RequestsDAL
from src.DAL.tokens import get_user
from src.database.user_roles import UserRole
from src.models import (
    DenyWorkerIn,
    RequestIn,
    RequestOut,
    WorkerInRequestIn,
    WorkerInRequestOut,
)
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

    @staticmethod
    async def send_request(req: Request, request_id: int) -> RequestOut:
        return await RequestsDAL.send_request(await get_user(req), request_id)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def accept_worker(
        req: Request, request_id: int, worker_id: int
    ) -> WorkerInRequestOut:
        return await RequestsDAL.accept_worker(request_id, worker_id)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def deny_worker(
        req: Request, request_id: int, worker_id: int, params: DenyWorkerIn
    ):
        return await RequestsDAL.deny_worker(request_id, worker_id, params)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def deny_worker(
        req: Request, request_id: int, worker_id: int, params: DenyWorkerIn
    ):
        return await RequestsDAL.deny_worker(request_id, worker_id, params)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def close(req: Request, request_id: int) -> RequestOut:
        return await RequestsDAL.close(request_id)

    @staticmethod
    @auth_required(UserRole.OPERATOR, check_id=False, auth_redirect=False)
    async def reset_worker_in_request(
        req: Request, request_id: int, worker_id: int
    ) -> WorkerInRequestOut:
        return await RequestsDAL.reset_worker_in_request_status(request_id, worker_id)
