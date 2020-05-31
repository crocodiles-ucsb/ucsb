from http import HTTPStatus
from typing import Awaitable, Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from src.DAL.utils import ListWithPagination, get_pagination
from src.database.database import create_session, run_in_threadpool
from src.database.models import (
    ContractorRepresentative,
    ObjectOfWork,
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
    RequestForTemplateOut,
    RequestIn,
    RequestOut,
    WorkerComplexOut,
    WorkerInListOut,
    WorkerInRequestOut,
    WorkerSimpleOut,
    WorkerSimpleOutWithRequestInfo,
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
                        and worker_request.status == WorkerInRequestStatus.ACCEPTED
                    ):
                        raise DALError(
                            HTTPStatus.BAD_REQUEST.value,
                            'Этот пользователь уже участвует в заявке по '
                            'этому документы и на этом участке',
                        )
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
                worker = session.query(Worker).filter(Worker.id == worker_id).one()
                for worker_in_request in request.workers_in_request:
                    if worker_in_request.worker == worker:
                        session.delete(worker_in_request)
                        return
                raise DALError(HTTPStatus.NOT_FOUND.value)
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)

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
            if len(request.workers_in_request) == 0:
                raise DALError(
                    HTTPStatus.BAD_REQUEST.value, 'Вы не можете создать пустую заявку'
                )
            if (
                request not in representative.contractor.requests
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
    def get_operator_request(request_id: int) -> Awaitable[RequestForTemplateOut]:
        with create_session() as session:
            request = RequestsDAL._get_request(request_id, session)
            return RequestsDAL._serialize_request(request)  # type: ignore

    @staticmethod
    @run_in_threadpool
    def get_operators_requests(
        substring: str, page: int, size: int
    ) -> Awaitable[ListWithPagination[RequestForTemplateOut]]:
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
                serialized_requests.append(RequestsDAL._serialize_request(request))
            return get_pagination(serialized_requests, page, size)  # type: ignore

    @staticmethod
    def serialize_worker(worker: Worker):
        return WorkerSimpleOut(
            id=worker.id,
            last_name=worker.last_name,
            first_name=worker.first_name,
            patronymic=worker.patronymic,
            profession=worker.profession.data,
            birth_date=worker.birth_date,
            violations_points=worker.penalty_points,
            contractor_name=worker.contractor.title,
            contractor_id=worker.contractor_id,
        )

    @staticmethod
    @run_in_threadpool
    def get_representative_workers(
        representative_id: int, substring: str, page: int, size: int
    ):
        with create_session() as session:
            try:
                representative: ContractorRepresentative = session.query(
                    ContractorRepresentative
                ).filter(ContractorRepresentative.id == representative_id).one()
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            return get_pagination(
                [
                    RequestsDAL.serialize_worker(worker)
                    for worker in representative.contractor.workers
                    if substring
                    and substring
                    in f'{worker.last_name} {worker.first_name} {worker.patronymic}'
                    or not substring
                ],
                page,
                size,
            )

    @staticmethod
    @run_in_threadpool
    def get_representative_workers_in_request(
        representative_id: int,
        request_id: int,
        substring: str,
        page: int,
        size: int,
        is_result: bool = False,
    ):
        with create_session() as session:
            request = RequestsDAL._get_request(request_id, session)

            try:
                representative: ContractorRepresentative = session.query(
                    ContractorRepresentative
                ).filter(ContractorRepresentative.id == representative_id).one()
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            if request not in representative.contractor.requests:
                raise DALError(HTTPStatus.FORBIDDEN.value)
            res = []
            was_broken: bool = False
            for worker in representative.contractor.workers:
                if was_broken:
                    was_broken = False
                if (
                    substring
                    and substring
                    not in f'{worker.last_name} {worker.first_name} {worker.patronymic}'
                ):
                    continue
                for worker_in_request in worker.worker_requests:
                    request_ = worker_in_request.request
                    if (
                        request_.object_of_work_id == request.object_of_work_id
                        and request_.contract_id == request.contract_id
                        and worker_in_request.status != WorkerInRequestStatus.CANCELLED
                    ):
                        was_broken = True
                        break
                if not was_broken:
                    res.append(RequestsDAL.serialize_worker(worker))
        return get_pagination(res, page, size)

    @staticmethod
    def serialize_worker_with_request_info(
        worker: Worker, worker_in_request: WorkerInRequest
    ):
        return WorkerSimpleOutWithRequestInfo(
            id=worker.id,
            last_name=worker.last_name,
            first_name=worker.first_name,
            patronymic=worker.patronymic,
            profession=worker.profession.data,
            birth_date=worker.birth_date,
            violations_points=worker.penalty_points,
            status=worker_in_request.status,
            comment=worker_in_request.comment if worker_in_request.comment else '',
            reason=worker_in_request.reason_for_rejection.data
            if worker_in_request.reason_for_rejection
            else '',
            contractor_name = worker.contractor.title,
            contractor_id=worker.contractor_id
        )

    @staticmethod
    @run_in_threadpool
    def get_operator_workers_in_request(
        request_id: int, substring: str, page: int, size: int, is_result: bool = False
    ) -> Awaitable[ListWithPagination[WorkerInListOut]]:

        with create_session() as session:
            request = RequestsDAL._get_request(request_id, session)
            workers = request.workers_in_request
            if substring:
                workers = [
                    worker
                    for worker in workers
                    if substring
                    in f'{worker.worker.last_name} {worker.worker.first_name} {worker.worker.patronymic}'
                ]
            workers_to_out = []
            if request.status != RequestStatus.WAITING_FOR_VERIFICATION:
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            for worker in workers:
                if (
                    not is_result
                    and worker.status != WorkerInRequestStatus.WAITING_FOR_VERIFICATION
                ):
                    continue
                if is_result and not (
                    worker.status == WorkerInRequestStatus.ACCEPTED
                    or worker.status == WorkerInRequestStatus.CANCELLED
                ):
                    continue
                workers_to_out.append(
                    WorkerInListOut(
                        last_name=worker.worker.last_name,
                        first_name=worker.worker.first_name,
                        patronymic=worker.worker.patronymic,
                        id=worker.id,
                        profession=worker.worker.profession.data,
                        penalty_points=worker.worker.penalty_points,
                        status=worker.status,
                        reason_of_rejection=worker.reason_for_rejection.data
                        if worker.reason_for_rejection
                        else None,
                    )
                )
        return get_pagination(workers_to_out, page, size)

    @staticmethod
    @run_in_threadpool
    def get_representative_request(request_id):
        with create_session() as session:
            request = RequestsDAL._get_request(request_id, session)
            return RequestsDAL._serialize_request(request)

    @staticmethod
    @run_in_threadpool
    def get_representative_request_result(
        request_id: int, representative_id: int, substring: str, page: int, size: int
    ):
        with create_session() as session:
            try:
                representative = (
                    session.query(ContractorRepresentative)
                    .filter(ContractorRepresentative.id == representative_id)
                    .one()
                )
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            request = RequestsDAL._get_request(request_id, session)
            if request not in representative.contractor.requests:
                raise DALError(HTTPStatus.FORBIDDEN.value)
            if request.status != RequestStatus.WAITING_FOR_READINESS:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            workers = map(
                lambda worker_in_request: worker_in_request.worker,
                request.workers_in_request,
            )
            res = [
                RequestsDAL.serialize_worker(worker)
                for worker in workers
                if substring
                and substring in f''
                f'{worker.last_name} {worker.first_name} {worker.patronymic}'
                or not substring
            ]
            return get_pagination(res, page, size)

    @staticmethod
    def _serialize_request(request: Request) -> RequestForTemplateOut:
        return RequestForTemplateOut(
            id=request.id,
            contractor_id=request.contractor.id,
            title_of_organization=request.contractor.title,
            name_of_object=request.object_of_work.data,
            workers_count=len(request.workers_in_request),
            status=request.status,
            contract_link=f'{Urls.base_url.value}/files/{request.contract.uuid}',
            contract_title=request.contract.title,
        )

    @staticmethod
    def _serialize_worker(worker: Worker) -> WorkerComplexOut:
        return WorkerComplexOut(
            id=worker.id,
            last_name=worker.last_name,
            first_name=worker.first_name,
            patronymic=worker.patronymic,
            profession=worker.profession.data,
            birth_date=worker.birth_date,
            identification_uuid=worker.identification.uuid,
            driving_license_uuid=worker.driving_license.uuid
            if worker.driving_license
            else None,
            order_of_acceptance_to_work_uuid=worker.order_of_acceptance_to_work.uuid
            if worker.order_of_acceptance_to_work
            else None,
            training_information_uuid=worker.training_information.uuid
            if worker.training_information
            else None,
            speciality_course_information_uuid=worker.speciality_course_information.uuid
            if worker.speciality_course_information
            else None,
            another_drive_license_uuid=worker.another_drive_license.uuid
            if worker.another_drive_license
            else None,
            medical_certificate_uuid=worker.medical_certificate.uuid
            if worker.medical_certificate
            else None,
            certificate_of_competency_uuid=worker.certificate_of_competency.uuid
            if worker.certificate_of_competency
            else None,
            instructed_information_uuid=worker.instructed_information.uuid
            if worker.instructed_information
            else None,
            emergency_driving_certificate_uuid=worker.emergency_driving_certificate.uuid
            if worker.emergency_driving_certificate
            else None,
            violations_points=worker.penalty_points,
            count_of_violations=len(worker.penalties),
        )

    @staticmethod
    @run_in_threadpool
    def get_worker(request_id: int, worker_id: int) -> Awaitable[WorkerComplexOut]:
        with create_session() as session:
            RequestsDAL._get_request(
                request_id, session
            )  # checking existence of request
            worker_in_request = RequestsDAL._get_worker(session, worker_id)
            if (
                worker_in_request.status
                != WorkerInRequestStatus.WAITING_FOR_VERIFICATION
            ):
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            worker = worker_in_request.worker
            res = RequestsDAL._serialize_worker(worker)
            res.id = worker_in_request.id
            return res  # type: ignore

    @staticmethod
    @run_in_threadpool
    def get_representative_requests(
        representative_id: int,
        substring: str,
        page: int,
        size: int,
        solved: bool = False,
    ) -> Awaitable[ListWithPagination[RequestForTemplateOut]]:
        with create_session() as session:
            try:
                representative: ContractorRepresentative = session.query(
                    ContractorRepresentative
                ).filter(ContractorRepresentative.id == representative_id).one()
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            res = []
            for request in representative.contractor.requests:
                if substring and substring not in request.object_of_work.data:
                    continue
                if solved and request.status != RequestStatus.CLOSED:
                    continue
                if (
                    not solved
                    and request.status != RequestStatus.WAITING_FOR_VERIFICATION
                ):
                    continue
                res.append(RequestsDAL._serialize_request(request))
            return get_pagination(res, page, size)

    @staticmethod
    @run_in_threadpool
    def get_worker_from_requests(
        representative_id: int, request_id: int, substring: str, page: int, size: int
    ):
        with create_session() as session:
            request = RequestsDAL._get_request(request_id, session)
            try:
                representative = (
                    session.query(ContractorRepresentative)
                    .filter(ContractorRepresentative.id == representative_id)
                    .one()
                )

            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            if request not in representative.contractor.requests:
                raise DALError(HTTPStatus.FORBIDDEN.value)
            res = []
            for worker_in_request in request.workers_in_request:
                worker = worker_in_request.worker
                if (
                    substring
                    and substring
                    not in f'{worker.last_name} {worker.first_name} {worker.patronymic}'
                ):
                    continue
                res.append(
                    RequestsDAL.serialize_worker_with_request_info(
                        worker, worker_in_request
                    )
                )
            return get_pagination(res, page, size)
