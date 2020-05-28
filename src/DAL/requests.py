from http import HTTPStatus
from typing import Awaitable, Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
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
from src.models import OutUser, RequestIn, RequestOut, WorkerInRequestOut


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
                Request.contract_id == params.contract_id
                and Request.object_of_work_id == params.object_of_work_id
                and Request.status == RequestStatus.WAITING_FOR_READINESS
                and Request.contractor_id == contractor_id
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
                request = session.query(Request).filter(Request.id == request_id).one()
                contractor = representative_from_db.contractor
                if worker_id not in map(lambda worker: worker.id, contractor.workers):
                    raise DALError(HTTPStatus.BAD_REQUEST.value)
                if request not in contractor.requests:
                    raise DALError(HTTPStatus.BAD_REQUEST.value)
                if worker_id in map(
                    lambda worker: worker.id, request.workers_in_request
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
            try:
                request = session.query(Request).filter(Request.id == request_id).one()
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
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
