from http import HTTPStatus
from typing import Awaitable, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from src.DAL.utils import ListWithPagination, get_pagination
from src.database.database import create_session, run_in_threadpool
from src.database.models import (
    ContractorRepresentative,
    Request,
    RequestStatus,
    Worker,
    WorkerInRequest,
    WorkerInRequestStatus,
)
from src.exceptions import DALError
from src.models import (
    DenyWorkerIn,
    OutUser,
    RequestIn,
    RequestInListOut,
    RequestOut,
    WorkerInRequestOut,
)
from src.urls import Urls


class RequestsDAL:
    @staticmethod
    @run_in_threadpool
    def add(representative: OutUser, params: RequestIn) -> Awaitable[RequestOut]:
        with create_session() as session:
            representative_from_db = RequestsDAL._get_contractor_representatives(
                representative, session
            )
            contractor_id = representative_from_db.contractor_id
            request: Optional[Request] = session.query(Request).filter(
                Request.contract_id == params.contract_id,
                Request.object_of_work_id == params.object_of_work_id,
                Request.status == RequestStatus.WAITING_FOR_READINESS,
                Request.contractor_id == contractor_id,
            ).first()
            if request:
                RequestsDAL._delete_old_request(request, session)
            request = Request(
                object_of_work_id=params.object_of_work_id,
                contract_id=params.contract_id,
                status=RequestStatus.WAITING_FOR_READINESS,
                contractor_id=contractor_id,
            )
            session.add(request)
            session.flush()
            return RequestOut.from_orm(request)  # type: ignore

    @staticmethod
    def _get_contractor_representatives(
        representative: OutUser, session: Session
    ) -> ContractorRepresentative:
        representative_from_db: ContractorRepresentative = session.query(
            ContractorRepresentative
        ).filter(ContractorRepresentative.id == representative.id).one()
        return representative_from_db

    @staticmethod
    def _delete_old_request(request: Request, session: Session) -> None:
        for worker in request.workers_in_request:  # type: ignore
            session.delete(worker)
        session.delete(request)

    @staticmethod
    @run_in_threadpool
    def add_worker_to_request(
        representative: OutUser, request_id: int, worker_id: int
    ) -> Awaitable[WorkerInRequestOut]:
        with create_session() as session:
            try:
                representative_from_db = RequestsDAL._get_contractor_representatives(
                    representative, session
                )
                request = RequestsDAL._get_request(request_id, session)
                contractor = representative_from_db.contractor
                worker = session.query(Worker).filter(Worker.id == worker_id).one()
                if worker not in contractor.workers:
                    raise DALError(HTTPStatus.BAD_REQUEST.value)
                if request not in contractor.requests:
                    raise DALError(HTTPStatus.BAD_REQUEST.value)
                if worker in request.workers_in_request:
                    raise DALError(HTTPStatus.BAD_REQUEST.value)
                for worker_request in worker.worker_requests:
                    request_: Request = worker_request.request
                    if (
                        request_.contract_id == request.contract_id
                        and request_.object_of_work_id == request.object_of_work_id
                        and request_.contractor_id == request.contractor_id
                    ):
                        raise DALError(HTTPStatus.BAD_REQUEST.value)
                worker_in_request = WorkerInRequest(
                    worker_id=worker_id,
                    request_id=request_id,
                    status=WorkerInRequestStatus.WAITING_FOR_READINESS,
                )
                session.add(worker_in_request)
                session.flush()
                return WorkerInRequestOut.from_orm(worker_in_request)  # type: ignore
            except NoResultFound:
                raise DALError(HTTPStatus.BAD_REQUEST.value)

    @staticmethod
    @run_in_threadpool
    def delete_worker_from_request(
        representative: OutUser, request_id: int, worker_id: int
    ) -> None:
        with create_session() as session:
            request = RequestsDAL._get_request(request_id, session)
            representative_from_db = RequestsDAL._get_contractor_representatives(
                representative, session
            )
            if request not in representative_from_db.contractor.requests:
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            try:
                worker_in_request = (
                    session.query(WorkerInRequest)
                    .filter(WorkerInRequest.id == worker_id)
                    .one()
                )
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            if worker_in_request not in request.workers_in_request:
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            session.delete(worker_in_request)

    @staticmethod
    def _get_request(request_id, session):
        try:
            request = session.query(Request).filter(Request.id == request_id).one()
        except NoResultFound:
            raise DALError(HTTPStatus.NOT_FOUND.value)
        return request

    @staticmethod
    @run_in_threadpool
    def send_request(representative: OutUser, request_id: int) -> Awaitable[RequestOut]:
        with create_session() as session:
            representative = RequestsDAL._get_contractor_representatives(
                representative, session
            )
            request = RequestsDAL._get_request(request_id, session)
            if (
                request not in representative.contractor.requests
                or len(request.workers_in_request) == 0
                or request.status != RequestStatus.WAITING_FOR_READINESS
            ):
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            request.status = RequestStatus.WAITING_FOR_VERIFICATION
            for worker in request.workers_in_request:
                worker.status = WorkerInRequestStatus.WAITING_FOR_VERIFICATION
            return RequestOut.from_orm(request)  # type: ignore

    @staticmethod
    @run_in_threadpool
    def accept_worker(request_id: int, worker_id: int) -> Awaitable[WorkerInRequestOut]:
        with create_session() as session:
            request = RequestsDAL._get_request(request_id, session)
            worker = RequestsDAL._get_worker(session, worker_id)
            RequestsDAL._validate_data(request, worker)
            worker.status = WorkerInRequestStatus.ACCEPTED
            return WorkerInRequestOut.from_orm(worker)

    @staticmethod
    @run_in_threadpool
    def deny_worker(
        request_id: int, worker_id: int, params: DenyWorkerIn
    ) -> Awaitable[WorkerInRequestOut]:
        with create_session() as session:
            request = RequestsDAL._get_request(request_id, session)
            worker = RequestsDAL._get_worker(session, worker_id)
            RequestsDAL._validate_data(request, worker)
            worker.status = WorkerInRequestStatus.CANCELLED
            worker.reason_for_rejection_id = params.reason_for_rejection_id
            if params.comment:
                worker.comment = params.comment
            return WorkerInRequestOut.from_orm(worker)  # type: ignore

    @staticmethod
    def _validate_data(request, worker):
        if request.status != RequestStatus.WAITING_FOR_VERIFICATION:
            raise DALError(HTTPStatus.BAD_REQUEST.value)
        if worker not in request.workers_in_request:
            raise DALError(HTTPStatus.BAD_REQUEST.value)
        if worker.status != WorkerInRequestStatus.WAITING_FOR_VERIFICATION:
            raise DALError(HTTPStatus.BAD_REQUEST.value)

    @staticmethod
    def _get_worker(session: Session, worker_id: int) -> WorkerInRequest:
        try:
            return (
                session.query(WorkerInRequest)
                .filter(WorkerInRequest.id == worker_id)
                .one()
            )
        except NoResultFound:
            raise DALError(HTTPStatus.BAD_REQUEST.value)

    @staticmethod
    @run_in_threadpool
    def close(request_id: int) -> Awaitable[RequestOut]:
        with create_session() as session:
            request = RequestsDAL._get_request(request_id, session)
            if request.status != RequestStatus.WAITING_FOR_VERIFICATION:
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            if WorkerInRequestStatus.WAITING_FOR_VERIFICATION in map(
                lambda worker: worker.status, request.workers_in_request
            ):
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            request.status = RequestStatus.CLOSED
            return RequestOut.from_orm(request)  # type: ignore

    @staticmethod
    @run_in_threadpool
    def reset_worker_in_request_status(
        request_id: int, worker_id: int
    ) -> Awaitable[WorkerInRequestOut]:
        with create_session() as session:
            worker = RequestsDAL._get_worker(session, worker_id)
            request = RequestsDAL._get_request(request_id, session)
            if worker not in request.workers_in_request:
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            if (
                worker.status != WorkerInRequestStatus.ACCEPTED
                and worker.status != WorkerInRequestStatus.CANCELLED
            ):
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            if worker.status == WorkerInRequestStatus.CANCELLED:
                worker.reason_for_rejection = None
                worker.comment = None
            worker.status = WorkerInRequestStatus.WAITING_FOR_VERIFICATION
            return WorkerInRequestOut.from_orm(worker)

    @staticmethod
    @run_in_threadpool
    def get_operators_requests(
        substring: str, page: int, size: int
    ) -> Awaitable[ListWithPagination[RequestInListOut]]:
        with create_session() as session:
            requests = (
                session.query(Request)
                .filter(Request.status == RequestStatus.WAITING_FOR_VERIFICATION)
                .all()
            )
            if substring:
                requests = [
                    request.contractor.title
                    for request in requests
                    if substring in request.contractor.title
                ]
            serialized_requests = []
            for request in requests:
                serialized_requests.append(
                    RequestInListOut(
                        id=request.id,
                        contractor_id=request.contractor.id,
                        title_of_organization=request.contractor.title,
                        name_of_object=request.object_of_work.data,
                        workers_count=len(request.workers_in_request),
                        contract_link=f'{Urls.base_url.value}/files/{request.contract.uuid}',
                        contract_title=request.contract.title
                    )
                )
            return get_pagination(serialized_requests, page, size)  # type: ignore
