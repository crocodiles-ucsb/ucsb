import pytest
from src.database.database import Base, engine


@pytest.fixture(scope='function', autouse=True)
def _init_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
