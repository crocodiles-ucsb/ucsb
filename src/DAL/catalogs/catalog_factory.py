from typing import Any, Type

from src.api.catalogs import CatalogType
from src.DAL.catalogs.abstract_catalog import AbstractCatalog, TOutData
from src.DAL.catalogs.objects_of_work import ObjectsOfWork
from src.DAL.catalogs.professions import Professions
from src.DAL.catalogs.reason_for_rejection_of_application import (
    ReasonsForRejectionOfApplication,
)
from src.DAL.catalogs.vehicles import Vehicles
from src.DAL.catalogs.violations import Violations


def get_catalog(
    catalog_type: CatalogType, out_model: Type[TOutData]
) -> AbstractCatalog[TOutData, Any]:
    if catalog_type.out_model != out_model:
        raise ValueError()
    if catalog_type == CatalogType.professions:
        return Professions()  # type: ignore
    if catalog_type == CatalogType.violations:
        return Violations()
    if catalog_type == CatalogType.reasons_for_rejection_of_application:
        return ReasonsForRejectionOfApplication()
    if catalog_type == CatalogType.vehicles:
        return Vehicles()
    if catalog_type == CatalogType.objects_of_work:
        return ObjectsOfWork()
    raise ValueError()
