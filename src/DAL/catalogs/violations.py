from typing import Optional, List

from src.DAL.adding_data_to_catalog import AbstractAddingDataToCatalog, AddingDataCatalogWithIntValue
from src.DAL.catalogs.abstract_catalog import AbstractCatalog
from src.DAL.getting_data_from_catalog import AbstractGettingDataFromCatalog, SimpleGettingDataFromCatalog
from src.api.catalogs import CatalogType
from src.models import CatalogWithIntValueIn, CatalogWithIntValueOut


class Violations(AbstractCatalog[CatalogWithIntValueOut, CatalogWithIntValueIn]):
    def __init__(self) -> None:
        self.getting_data: AbstractGettingDataFromCatalog[
            CatalogWithIntValueOut
        ] = SimpleGettingDataFromCatalog[CatalogWithIntValueOut]()
        self.adding_data: AbstractAddingDataToCatalog[
            CatalogWithIntValueIn, CatalogWithIntValueOut
        ] = AddingDataCatalogWithIntValue()

    async def add_data(self, params: CatalogWithIntValueIn) -> CatalogWithIntValueOut:
        return await self.adding_data.add(
            CatalogType.violations, params, CatalogWithIntValueOut
        )

    async def get_data(self, substring: Optional[str]) -> List[CatalogWithIntValueOut]:
        return await self.getting_data.get_data(
            CatalogType.violations, substring, CatalogWithIntValueOut
        )
