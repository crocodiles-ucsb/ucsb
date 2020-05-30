from datetime import date
from http import HTTPStatus
from typing import Awaitable

from sqlalchemy.orm.exc import NoResultFound
from src.DAL.documents_dal import DocumentsDAL
from src.DAL.requests import RequestsDAL
from src.DAL.users.contractor_representative import (
    ContractorRepresentativeAddingParams,
    ContractorRepresentatives,
    ContractorRepresentativeToAddingOut,
)
from src.database.database import create_session, run_in_threadpool
from src.database.models import ContractorRepresentative, Profession, Worker
from src.exceptions import DALError
from src.messages import Message
from src.models import (
    ContractorRepresentativeOut,
    OutUser,
    SimpleDocumentIn,
    WorkerComplexOut,
    WorkerOut,
    WorkerWithProfessionOut,
)


class RepresentativesDAL:
    @staticmethod
    async def add_worker(
        contractor_representative: OutUser,
        last_name: str,
        first_name: str,
        patronymic: str,
        birthday: date,
        profession: str,
        **kwargs
    ) -> WorkerWithProfessionOut:
        with create_session() as session:
            try:
                profession = (
                    session.query(Profession)
                    .filter(Profession.data == profession)
                    .one()
                )
            except NoResultFound:
                raise DALError(
                    HTTPStatus.BAD_REQUEST.value,
                    Message.PROFESSION_DOES_NOT_EXITS.value,
                )
            contractor_representative_from_db = await RepresentativesDAL._get_contractor_representative(
                contractor_representative, session
            )
            worker = Worker(
                patronymic=patronymic,
                last_name=last_name,
                first_name=first_name,
                birth_date=birthday,
                profession=profession,
                contractor_id=contractor_representative_from_db.contractor_id,
            )
            for key, value in kwargs.items():
                if hasattr(Worker, key) and value:
                    await DocumentsDAL.add_worker_document(
                        session, worker, key, SimpleDocumentIn(file=value)
                    )
            session.flush()
            worker_out = WorkerOut.from_orm(worker)
            return WorkerWithProfessionOut(
                **worker_out.dict(), profession=worker.profession.data
            )

    @staticmethod
    async def _get_contractor_representative(contractor_representative, session):
        contractor_representative_from_db: ContractorRepresentative = session.query(
            ContractorRepresentative
        ).filter(ContractorRepresentative.id == contractor_representative.id).first()
        if not contractor_representative_from_db:
            raise DALError(
                HTTPStatus.BAD_REQUEST.value, 'contractor representative not found'
            )
        return contractor_representative_from_db

    @staticmethod
    async def add(
        params: ContractorRepresentativeAddingParams,
    ) -> ContractorRepresentativeToAddingOut:
        return await ContractorRepresentatives().add_user(params)

    @staticmethod
    @run_in_threadpool
    def get_worker(
        representative_id: int, worker_id: int
    ) -> Awaitable[WorkerComplexOut]:
        with create_session() as session:
            try:
                representative: ContractorRepresentative = (
                    session.query(ContractorRepresentative)
                    .filter(ContractorRepresentative.id == representative_id)
                    .one()
                )
                worker: Worker = session.query(Worker).filter(
                    Worker.id == worker_id
                ).one()
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            if worker not in representative.contractor.workers:
                raise DALError(HTTPStatus.FORBIDDEN.value)
            return RequestsDAL._serialize_worker(worker)
