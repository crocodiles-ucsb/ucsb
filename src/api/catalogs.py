from enum import Enum
from typing import Type

from pydantic import BaseModel
from src.models import CatalogWithIntValueOut, SimpleCatalogOut


class CatalogStructureType(Enum):
    simple = 'simple'
    int_value = 'int_value'


class CatalogType(Enum):
    professions = 'profession'
    vehicles = 'vehicle'
    objects_of_work = 'object_of_work'
    reasons_for_rejection_of_application = 'reason_for_rejection_of_application'
    violations = 'violation'

    @property
    def html(self) -> str:
        try:
            return _htmls[self]
        except IndexError:
            raise ValueError()

    @property
    def out_model(self) -> Type[BaseModel]:
        try:
            return _out_models[self]
        except IndexError:
            raise ValueError()

    def structure_type(self) -> CatalogStructureType:
        try:
            return _catalog_structure_type[self]
        except IndexError:
            raise ValueError()

    @property
    def description(self) -> str:
        try:
            return _description_on_russian[self]
        except IndexError:
            raise ValueError()


_htmls = {
    CatalogType.professions: 'admin-simple-catalog.html',
    CatalogType.vehicles: 'admin-simple-catalog.html',
    CatalogType.objects_of_work: 'admin-simple-catalog.html',
    CatalogType.reasons_for_rejection_of_application: 'admin-simple-catalog.html',
    CatalogType.violations: 'admin-catalog-with-int-value.html',
}
_description_on_russian = {
    CatalogType.professions: 'Профессия',
    CatalogType.vehicles: 'Вид транспорта',
    CatalogType.objects_of_work: 'Объект работы',
    CatalogType.reasons_for_rejection_of_application: 'Причина отклонения заявки',
    CatalogType.violations: 'Нарушение',
}

_out_models = {
    CatalogType.professions: SimpleCatalogOut,
    CatalogType.vehicles: SimpleCatalogOut,
    CatalogType.objects_of_work: SimpleCatalogOut,
    CatalogType.reasons_for_rejection_of_application: SimpleCatalogOut,
    CatalogType.violations: CatalogWithIntValueOut,
}
_catalog_structure_type = {
    CatalogType.professions: CatalogStructureType.simple,
    CatalogType.vehicles: CatalogStructureType.simple,
    CatalogType.objects_of_work: CatalogStructureType.simple,
    CatalogType.reasons_for_rejection_of_application: CatalogStructureType.simple,
    CatalogType.violations: CatalogStructureType.int_value,
}
