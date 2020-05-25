from datetime import datetime
from http import HTTPStatus

from sqlalchemy.orm.exc import NoResultFound
from src.DAL.documents_dal import DocumentsDAL
from src.database.database import create_session
from src.database.models import Profession, Worker
from src.exceptions import DALError
from src.messages import Message
from src.models import SimpleDocumentIn


class RepresentativesDAL:
    @staticmethod
    async def add_worker(
        last_name: str, first_name: str, birthday: datetime, profession: str, **kwargs
    ) -> None:
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
            worker = Worker(
                last_name=last_name,
                first_name=first_name,
                birth_date=birthday,
                profession=profession,
            )
            for key, value in kwargs.items():
                if hasattr(Worker, key):
                    await DocumentsDAL.add_worker_document(
                        session, worker, key, SimpleDocumentIn(file=value)
                    )
