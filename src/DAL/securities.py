from datetime import date
from http import HTTPStatus
from typing import Awaitable, List

from src.DAL.requests import RequestsDAL
from src.DAL.utils import ListWithPagination, get_pagination
from src.database.database import create_session, run_in_threadpool
from src.database.models import Worker, Penalty
from src.exceptions import DALError
from src.models import WorkerSimpleOut, WorkerComplexOut, WorkerPenaltyOut, PenaltyIn


class SecuritiesDAL:
    @staticmethod
    @run_in_threadpool
    def get_workers(
            substring: str, page: int, size: int
    ) -> Awaitable[ListWithPagination[WorkerSimpleOut]]:
        with create_session() as session:
            workers = session.query(Worker).all()
            res = []
            for worker in workers:
                if (
                        substring
                        and substring
                        in f'{worker.last_name} {worker.first_name} {worker.patronymic}' or not substring
                ):
                    res.append(RequestsDAL.serialize_worker(worker))

        return get_pagination(res, page, size)

    @staticmethod
    @run_in_threadpool
    def get_worker(worker_id: int) -> WorkerComplexOut:
        with create_session() as session:
            worker = SecuritiesDAL._get_worker(session, worker_id)
            return RequestsDAL._serialize_worker(worker)

    @staticmethod
    def _get_worker(session, worker_id):
        worker = session.query(Worker).filter(Worker.id == worker_id).first()
        if not worker:
            raise DALError(HTTPStatus.NOT_FOUND.value)
        return worker

    @staticmethod
    @run_in_threadpool
    def get_worker_violations(worker_id: int) -> List[WorkerPenaltyOut]:
        with create_session() as session:
            worker = SecuritiesDAL._get_worker(session, worker_id)
            return [WorkerPenaltyOut(created_at=penalty.created_at, data=penalty.violation.data,
                                     value=penalty.violation.value, object=penalty.object_of_work.data) for penalty in
                    worker.penalties]

    @staticmethod
    @run_in_threadpool
    def add_penalty(worker_id: int, params: PenaltyIn):
        with create_session() as session:
            worker = SecuritiesDAL._get_worker(session, worker_id)
            penalty = Penalty(violation_id=params.violation_id, worker_id=worker_id,
                              object_of_work_id=params.object_of_work_id, created_at=date.today())
            session.add(penalty)
            session.flush()
            worker.penalty_points = worker.penalty_points + penalty.violation.value

