from datetime import datetime

import pytest
from src.DAL.documents.abstract_document import DocumentParams
from src.DAL.documents.worker_document import WorkerDocument
from src.database.database import create_session
from src.database.models import Identification, Worker
from src.models import SimpleDocumentIn


@pytest.mark.asyncio
@pytest.mark.usefixtures('_mock_uuid')
async def test_save_file(upload_file, storage_path, uuid4):
    await WorkerDocument.save_file(upload_file)
    file_path = storage_path / f'{uuid4}.pdf'
    assert file_path.exists()
    with file_path.open('rb') as f:
        await upload_file.seek(0)
        assert await upload_file.read() == f.read()


@pytest.mark.asyncio
@pytest.mark.usefixtures('_patch_save_file', '_mock_uuid')
async def test_worker_document_adding(worker_document, upload_file, uuid4, path):
    WorkerDocument.save_file.return_value = DocumentParams(path, uuid4)
    with create_session() as session:
        worker = Worker(
            last_name='1', first_name='2', patronymic='3', birth_date=datetime.utcnow()
        )
        await worker_document.add(
            session, worker, 'identification', SimpleDocumentIn(file=upload_file)
        )
    with create_session() as session:
        identification = (
            session.query(Identification).filter(Identification.id == 1).one()
        )
        worker = session.query(Worker).filter(Worker.id == 1).one()
        assert worker.identification == identification
        assert identification.path_to_document == str(path)
        assert identification.uuid == uuid4
        assert identification.worker == worker
