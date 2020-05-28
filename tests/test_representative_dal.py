from pathlib import Path

import pytest
from src.DAL.documents.abstract_document import AbstractDocument, DocumentParams
from src.DAL.representatives_dal import RepresentativesDAL
from src.database.database import create_session
from src.database.models import Worker
from src.exceptions import DALError
from src.messages import Message
from src.models import OutUser


@pytest.fixture()
def out_user():
    return OutUser(id=2, type='contractor_representative', username='123')


@pytest.fixture()
def _mock_contractor_representative(mocker, contractor):
    mocker.patch.object(RepresentativesDAL, '_get_contractor_representative')
    RepresentativesDAL._get_contractor_representative.return_value.contractor_id = (
        contractor.id
    )


@pytest.mark.asyncio
@pytest.mark.usefixtures('_mock_contractor_representative')
async def test_add_with_not_existence_profession_will_raise_error(
    worker_fields, out_user
):
    with pytest.raises(DALError) as e:
        await RepresentativesDAL.add_worker(
            **worker_fields,
            profession='not existence profession',
            contractor_representative=out_user
        )
    assert e.value.detail == Message.PROFESSION_DOES_NOT_EXITS.value


@pytest.mark.asyncio
@pytest.mark.usefixtures('_add_profession', '_mock_contractor_representative')
async def test_add_with_real_profession_will_raise_error(
    out_user, worker_fields, profession
):
    await RepresentativesDAL.add_worker(
        **worker_fields, profession=profession, contractor_representative=out_user
    )
    with create_session() as session:
        worker = session.query(Worker).filter(Worker.id == 1).first()
        assert worker.profession.data == profession


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_mock_contractor_representative',
    '_add_profession',
    '_mock_uuid',
    '_patch_save_file',
)
async def test_add_with_one_document(
    upload_file, worker_fields, profession, path, uuid4
):
    AbstractDocument.save_file.return_value = DocumentParams(path, uuid4)
    await RepresentativesDAL.add_worker(
        **worker_fields,
        profession=profession,
        identification=upload_file,
        contractor_representative=out_user
    )
    with create_session() as session:
        worker = session.query(Worker).filter(Worker.id == 1).one()
        assert worker.identification.path_to_document == str(path)
        assert worker.identification.uuid == uuid4


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_mock_contractor_representative',
    '_add_profession',
    '_mock_uuid',
    '_patch_save_file',
)
async def test_add_with_multiple_documents(
    upload_file, worker_fields, profession, path, uuid4, out_user
):
    another_path = Path() / '1'
    AbstractDocument.save_file.side_effect = [
        DocumentParams(path, uuid4),
        DocumentParams(another_path, uuid4),
    ]
    await RepresentativesDAL.add_worker(
        **worker_fields,
        profession=profession,
        identification=upload_file,
        driving_license=upload_file,
        contractor_representative=out_user
    )
    with create_session() as session:
        worker = session.query(Worker).filter(Worker.id == 1).one()
        assert worker.identification.path_to_document == str(path)
        assert worker.driving_license.path_to_document == str(another_path)
