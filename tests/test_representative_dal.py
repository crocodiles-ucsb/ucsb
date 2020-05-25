from datetime import datetime
from pathlib import Path

import pytest
from src.DAL.documents.abstract_document import AbstractDocument, DocumentParams
from src.DAL.representatives_dal import RepresentativesDAL
from src.database.database import create_session
from src.database.models import Profession, Worker
from src.exceptions import DALError
from src.messages import Message


@pytest.fixture()
def representatives_fields():
    return {'last_name': '1', 'first_name': '2', 'birthday': datetime.utcnow()}


@pytest.mark.asyncio
async def test_add_with_not_existence_profession_will_raise_error(
    representatives_fields,
):
    with pytest.raises(DALError) as e:
        await RepresentativesDAL.add_worker(
            **representatives_fields, profession='not existence profession'
        )
    assert e.value.detail == Message.PROFESSION_DOES_NOT_EXITS.value


@pytest.fixture()
def profession():
    return 'profession'


@pytest.fixture()
def _add_profession(profession):
    with create_session() as session:
        prof_name = profession
        session.add(Profession(data=prof_name))


@pytest.mark.asyncio
@pytest.mark.usefixtures('_add_profession')
async def test_add_with_real_profession_will_raise_error(
    representatives_fields, profession
):
    await RepresentativesDAL.add_worker(**representatives_fields, profession=profession)
    with create_session() as session:
        worker = session.query(Worker).filter(Worker.id == 1).first()
        assert worker.profession.data == profession


@pytest.mark.asyncio
@pytest.mark.usefixtures('_add_profession', '_mock_uuid', '_patch_save_file')
async def test_add_with_one_document(
    upload_file, representatives_fields, profession, path, uuid4
):
    AbstractDocument.save_file.return_value = DocumentParams(path, uuid4)
    await RepresentativesDAL.add_worker(
        **representatives_fields, profession=profession, identification=upload_file
    )
    with create_session() as session:
        worker = session.query(Worker).filter(Worker.id == 1).one()
        assert worker.identification.path_to_document == str(path)
        assert worker.identification.uuid == uuid4


@pytest.mark.asyncio
@pytest.mark.usefixtures('_add_profession', '_mock_uuid', '_patch_save_file')
async def test_add_with_multiple_documents(
    upload_file, representatives_fields, profession, path, uuid4
):
    another_path = Path() / '1'
    AbstractDocument.save_file.side_effect = [
        DocumentParams(path, uuid4),
        DocumentParams(another_path, uuid4),
    ]
    await RepresentativesDAL.add_worker(
        **representatives_fields,
        profession=profession,
        identification=upload_file,
        driving_license=upload_file
    )
    with create_session() as session:
        worker = session.query(Worker).filter(Worker.id == 1).one()
        assert worker.identification.path_to_document == str(path)
        assert worker.driving_license.path_to_document == str(another_path)
