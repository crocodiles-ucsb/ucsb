from sqlalchemy.orm import Session
from src.DAL.documents.worker_document import WorkerDocument
from src.database.models import Worker
from src.models import SimpleDocumentIn


class DocumentsDAL:
    @staticmethod
    async def add_worker_document(
        session: Session, db_obj: Worker, document_type: str, params: SimpleDocumentIn
    ) -> None:
        await WorkerDocument().add(session, db_obj, document_type, params)
