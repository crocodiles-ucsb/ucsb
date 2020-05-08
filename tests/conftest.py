import pytest
from src.DAL.registration import SimpleRegistration, SimpleRegistrationParams
from src.database.database import Base, engine
from src.database.user_roles import UserRole
from src.models import InUser


@pytest.fixture(scope='function', autouse=True)
def _init_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def username():
    return 'username'


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
