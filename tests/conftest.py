from io import BytesIO
from pathlib import Path

import pytest
from fastapi import UploadFile
from src.config import storage_settings
from src.DAL.adding_user import AddingUserWithDisposableLink
from src.DAL.documents.abstract_document import AbstractDocument
from src.DAL.documents.worker_document import WorkerDocument
from src.DAL.registration import SimpleRegistration, SimpleRegistrationParams
from src.DAL.users.operator import OperatorAddingParams, OperatorToAddingOut
from src.database.database import Base, engine
from src.database.user_roles import UserRole
from src.models import InUser


@pytest.fixture(scope='function', autouse=True)
def _init_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def rmtree(root: Path) -> None:
    if not root.exists():
        return
    for p in root.iterdir():
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()

    root.rmdir()


@pytest.fixture()
def upload_file(resources_path) -> UploadFile:
    with (resources_path / 'test.pdf').open('rb') as f:
        bytes_ = BytesIO(f.read())
    return UploadFile('test.pdf', bytes_)


@pytest.fixture()
def worker_document():
    return WorkerDocument()


@pytest.fixture()
def _patch_save_file(mocker):
    mocker.patch.object(AbstractDocument, 'save_file')


@pytest.fixture()
def uuid4():
    return 'uuid'


@pytest.fixture()
def _mock_uuid(uuid4, mocker):
    mocker.patch('src.DAL.documents.abstract_document.uuid4').return_value = uuid4


@pytest.fixture()
def resources_path() -> Path:
    return Path(__file__).resolve().parent / 'resources'


@pytest.fixture(autouse=True)
def _clear_storage(storage_path):
    rmtree(storage_path)
    yield
    rmtree(storage_path)


@pytest.fixture(scope='session')
def username():
    return 'username'


@pytest.fixture()
def storage_path() -> Path:
    return Path(__file__).resolve().parent.parent / storage_settings.main_directory_name


@pytest.fixture(scope='session')
def password():
    return 'password'


@pytest.fixture()
def in_user(username, password):
    return InUser(username=username, password=password)


@pytest.fixture()
async def _add_user(simple_registration, simple_registration_params):
    await simple_registration.register(simple_registration_params)


@pytest.fixture(scope='session')
def simple_registration_params(username, password):
    return SimpleRegistrationParams(
        username=username, password=password, type=UserRole.ADMIN
    )


@pytest.fixture(scope='session')
def simple_registration():
    return SimpleRegistration()


@pytest.fixture(scope='session')
def adding_user_with_disposable_link():
    return AddingUserWithDisposableLink[OperatorAddingParams, OperatorToAddingOut]()


@pytest.fixture()
def operator_adding_params():
    return OperatorAddingParams(last_name='1', first_name='2')


@pytest.fixture()
def path():
    return Path(__file__)
