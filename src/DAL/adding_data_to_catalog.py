from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Awaitable, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from src.api.catalogs import CatalogType
from src.DAL.utils import get_catalog_db_obj
from src.database.database import create_session, run_in_threadpool
from src.exceptions import DALError
from src.messages import Message
from src.models import (
    CatalogWithIntValueIn,
    CatalogWithIntValueOut,
    SimpleCatalogIn,
    SimpleCatalogOut,
)

TAddParams = TypeVar('TAddParams')
TOut = TypeVar('TOut', bound=BaseModel)


class AbstractAddingDataToCatalog(Generic[TAddParams, TOut], ABC):
    @abstractmethod
    @run_in_threadpool
    def add(
        self, catalog_type: CatalogType, params: TAddParams, out_model: Type[TOut]
    ) -> Awaitable[TOut]:
        pass

    def _check_data(self, data: str) -> None:
        if data == '':
            raise DALError(Message.INVALID_CATALOG_VALUE.value)

    def _add_obj_to_db(
        self, catalog_type: CatalogType, out_model: Type[TOut], **kwargs
    ) -> TOut:
        db_obj = get_catalog_db_obj(catalog_type)
        with create_session() as session:
            obj = db_obj(**kwargs)
            session.add(obj)
            try:
                session.flush()
                return out_model.from_orm(obj)
            except IntegrityError:
                raise DALError(
                    HTTPStatus.BAD_REQUEST.value,
                    Message.ELEMENT_OF_CATALOG_ALREADY_EXISTS.value,
                )


class SimpleAddingDataToCatalog(
    AbstractAddingDataToCatalog[SimpleCatalogIn, SimpleCatalogOut]
):
    @run_in_threadpool
    def add(
        self,
        catalog_type: CatalogType,
        params: SimpleCatalogIn,
        out_model: Type[SimpleCatalogOut],
    ) -> Awaitable[SimpleCatalogOut]:
        self._check_data(params.data)
        return self._add_obj_to_db(catalog_type, out_model, **params.dict())


class AddingDataCatalogWithIntValue(
    AbstractAddingDataToCatalog[CatalogWithIntValueIn, CatalogWithIntValueOut]
):
    @run_in_threadpool
    def add(
        self,
        catalog_type: CatalogType,
        params: CatalogWithIntValueIn,
        out_model: Type[CatalogWithIntValueOut],
    ) -> Awaitable[CatalogWithIntValueOut]:
        if params.value <= 0:
            raise DALError(
                HTTPStatus.BAD_REQUEST.value, Message.INVALID_CATALOG_VALUE.value
            )
        self._check_data(params.data)
        return self._add_obj_to_db(catalog_type, out_model, **params.dict())
