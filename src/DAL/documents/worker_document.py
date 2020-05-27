from sqlalchemy.orm import Session
from src.DAL.documents.abstract_document import AbstractDocument
from src.DAL.utils import get_document_db_type
from src.database.models import Worker
from src.models import SimpleDocumentIn, SimpleDocumentOut


class WorkerDocument(AbstractDocument[SimpleDocumentIn, Worker, SimpleDocumentOut]):
    async def add(
        self,
        session: Session,
        db_obj: Worker,
        document_type: str,
        params: SimpleDocumentIn,
    ) -> SimpleDocumentOut:
        file_params = await self.save_file(params.file)
        document_db_model = get_document_db_type(document_type)
        document = document_db_model(
            path_to_document=str(file_params.path), uuid=file_params.uuid
        )
        session.add(document)
        document.worker = db_obj
        return SimpleDocumentOut.from_orm(document)
