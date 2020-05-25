from abc import ABC, abstractmethod
from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from typing import Awaitable, Generic, TypeVar
from uuid import uuid4

from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from src.config import storage_settings
from src.DAL.utils import get_document_out_model
from src.database.database import create_session, run_in_threadpool
from src.database.models import Document
from src.exceptions import DALError

TInput = TypeVar('TInput')
TDbObj = TypeVar('TDbObj')
TOutModel = TypeVar('TOutModel', bound=BaseModel)


@dataclass
class DocumentParams:
    path: Path
    uuid: str


class AbstractDocument(Generic[TInput, TDbObj, TOutModel], ABC):
    @abstractmethod
    async def add(
        self, session: Session, db_obj: TDbObj, document_type: str, params: TInput
    ) -> None:
        pass

    @run_in_threadpool
    def get(self, uuid: str) -> Awaitable[TOutModel]:
        with create_session() as session:
            try:
                document = session.query(Document).filter(Document.uuid == uuid).one()
                out_model = get_document_out_model(document.type)
                return out_model.from_orm(document)  # type: ignore
            except NoResultFound:
                raise DALError(HTTPStatus.NOT_FOUND.value)

    @staticmethod
    async def save_file(file: UploadFile) -> DocumentParams:
        current_path = Path(__file__).resolve()
        storage_folder_path: Path = current_path.parent.parent.parent.parent / storage_settings.main_directory_name
        if not storage_folder_path.exists():
            storage_folder_path.mkdir()
        data = await file.read()
        uuid = str(uuid4())
        file_name = f'{uuid}.pdf'
        file_path = storage_folder_path / file_name
        with file_path.open('wb') as f:
            f.write(data)
        return DocumentParams(file_path, uuid)
