from datetime import date
from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound
from src.DAL.documents_dal import DocumentsDAL
from src.DAL.tokens import get_user
from src.DAL.users.contractor_representative import (
    ContractorRepresentativeAddingParams,
    ContractorRepresentatives,
    ContractorRepresentativeToAddingOut,
)
from src.database.database import create_session
from src.database.models import ContractorRepresentative, Profession, Worker
from src.exceptions import DALError
from src.messages import Message
from src.models import (
    ContractorRepresentativeOut,
    SimpleDocumentIn,
    WorkerOut,
    WorkerWithProfessionOut,
)
from starlette.requests import Request


class RepresentativesDAL:
    @staticmethod
    async def add_worker(
        req: Request,
        last_name: str,
        first_name: str,
        birthday: date,
        profession: str,
        **kwargs
    ) -> WorkerWithProfessionOut:
        contractor_representative = await get_user(req)
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
            contractor_representative_from_db: ContractorRepresentative = session.query(
                ContractorRepresentative
            ).filter(
                ContractorRepresentative.id == contractor_representative.id
            ).first()
            if not contractor_representative_from_db:
                raise DALError(
                    HTTPStatus.BAD_REQUEST.value, 'contractor representative not found'
                )
            worker = Worker(
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
    async def add(
        params: ContractorRepresentativeAddingParams,
    ) -> ContractorRepresentativeToAddingOut:
        return await ContractorRepresentatives().add_user(params)
