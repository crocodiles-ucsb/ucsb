from http import HTTPStatus
from typing import Awaitable, Optional, Type, TypeVar

from sqlalchemy.orm.exc import NoResultFound
from src.api.catalogs import CatalogStructureType, CatalogType
from src.DAL.catalogs.catalog_factory import get_catalog
from src.DAL.utils import ListWithPagination, get_pagination
from src.database.database import create_session, run_in_threadpool
from src.database.models import Catalog
from src.exceptions import DALError
from src.messages import Message
from src.models import CatalogWithIntValueIn, SimpleCatalogIn


class CatalogsDAL:
    T = TypeVar('T')

    @staticmethod
    async def get_items(
        catalog_type: CatalogType,
        out_model: Type[T],
        page: int,
        substring: Optional[str],
        size: int = 10,
    ) -> ListWithPagination[T]:
        catalog = get_catalog(catalog_type, out_model)
        data = await catalog.get_data(substring)
        return get_pagination(data, page, size)

    @staticmethod
    async def add_item(
        catalog_type: CatalogType, data: str, value: Optional[int], out_model: Type[T]
    ) -> T:
        catalog = get_catalog(catalog_type, out_model)
        if catalog_type.structure_type() == CatalogStructureType.int_value:
            if value is None:
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            return await catalog.add_data(CatalogWithIntValueIn(data=data, value=value))

        return await catalog.add_data(SimpleCatalogIn(data=data))

    @staticmethod
    @run_in_threadpool
    def delete_catalog(catalog_id: int) -> Awaitable[None]:  # type: ignore
        with create_session() as session:
            try:
                catalog = session.query(Catalog).filter(Catalog.id == catalog_id).one()
                session.delete(catalog)
            except NoResultFound:
                raise DALError(
                    HTTPStatus.NOT_FOUND.value, Message.CATALOG_DOES_NOT_EXISTS.value
                )
