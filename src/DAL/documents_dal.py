from http import HTTPStatus
from typing import Awaitable, cast

from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from src.DAL.documents.contract import ContractDocument
from src.DAL.documents.contractor_document import ContractorDocument
from src.DAL.documents.worker_document import WorkerDocument
from src.database.database import create_session, run_in_threadpool
from src.database.models import Contract, Contractor, Document, Worker
from src.exceptions import DALError
from src.models import DocumentWithTitleIn, DocumentWithTitleOut, SimpleDocumentIn
from starlette.responses import FileResponse


class DocumentsDAL:
    @staticmethod
    async def add_worker_document(
        session: Session, db_obj: Worker, document_type: str, params: SimpleDocumentIn
    ) -> None:
        await WorkerDocument().add(session, db_obj, document_type, params)

    @staticmethod
    async def add_contractor_document(
        session: Session,
        db_obj: Contractor,
        document_type: str,
        params: SimpleDocumentIn,
    ):
        await ContractorDocument().add(session, db_obj, document_type, params)

    @staticmethod
    async def add_contract(
        contractor_id: int, title: str, file: UploadFile
    ) -> DocumentWithTitleOut:
        with create_session() as session:
            try:
                contractor = (
                    session.query(Contractor)
                    .filter(Contractor.id == contractor_id)
                    .one()
                )
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            return await ContractDocument().add(
                session,
                contractor,
                'contract',
                DocumentWithTitleIn(file=file, title=title),
            )

    @staticmethod
    @run_in_threadpool
    def get(file_id: str) -> Awaitable[FileResponse]:
        with create_session() as session:
            try:
                file: Document = session.query(Document).filter(
                    Document.uuid == file_id
                ).one()
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)
            if file.type == 'contract':
                file = cast(Contract, file)
                return FileResponse(file.path_to_document, filename=file.title + '.pdf')  # type: ignore
            return FileResponse(file.path_to_document)  # type: ignore
