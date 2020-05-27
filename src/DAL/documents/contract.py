from sqlalchemy.orm import Session
from src.DAL.documents.abstract_document import AbstractDocument, TDbObj
from src.DAL.utils import get_document_db_type
from src.database.models import Contractor
from src.models import DocumentWithTitleIn, DocumentWithTitleOut


class ContractDocument(
    AbstractDocument[DocumentWithTitleIn, Contractor, DocumentWithTitleOut]
):
    async def add(
        self,
        session: Session,
        db_obj: TDbObj,
        document_type: str,
        params: DocumentWithTitleIn,
    ) -> DocumentWithTitleOut:
        file_params = await self.save_file(params.file)
        document_db_model = get_document_db_type(document_type)
        document = document_db_model(
            title=params.title,
            path_to_document=str(file_params.path),
            uuid=file_params.uuid,
        )
        session.add(document)
        document.contractor = db_obj
        session.flush()
        return DocumentWithTitleOut.from_orm(document)
