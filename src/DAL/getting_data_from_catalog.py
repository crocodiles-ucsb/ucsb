from abc import ABC, abstractmethod
from typing import Awaitable, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session
from src.api.catalogs import CatalogType
from src.database.database import create_session, run_in_threadpool
from src.database.models import Catalog

TOutData = TypeVar('TOutData')


class AbstractGettingDataFromCatalog(Generic[TOutData], ABC):
    @abstractmethod
    @run_in_threadpool
    def get_data(
        self, catalog_type: CatalogType, substring: Optional[str], out: Type[TOutData]
    ) -> Awaitable[List[TOutData]]:
        pass

    def _get_catalog_from_db(
        self, catalog_type: CatalogType, session: Session, substring: Optional[str]
    ) -> List[Catalog]:
        items = session.query(Catalog).filter(Catalog.type == catalog_type.value).all()
        if substring:
            return [item for item in items if substring in item.data]
        return items

    def _get_items(self, catalog_type, out, substring):
        with create_session() as session:
            res = self._get_catalog_from_db(catalog_type, session, substring)
            return [out.from_orm(item) for item in res]  # type: ignore


class SimpleGettingDataFromCatalog(
    Generic[TOutData], AbstractGettingDataFromCatalog[TOutData]
):
    @run_in_threadpool
    def get_data(
        self, catalog_type: CatalogType, substring: Optional[str], out: Type[TOutData],
    ) -> Awaitable[List[TOutData]]:
        return self._get_items(catalog_type, out, substring)
