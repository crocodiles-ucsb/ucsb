from typing import Optional, List

from src.DAL.adding_data_to_catalog import AbstractAddingDataToCatalog, SimpleAddingDataToCatalog
from src.DAL.catalogs.abstract_catalog import AbstractCatalog
from src.DAL.getting_data_from_catalog import AbstractGettingDataFromCatalog, SimpleGettingDataFromCatalog
from src.api.catalogs import CatalogType
from src.models import SimpleCatalogOut, SimpleCatalogIn


class Vehicles(AbstractCatalog[SimpleCatalogOut, SimpleCatalogIn]):
    def __init__(self) -> None:
        self.getting_data: AbstractGettingDataFromCatalog[
            SimpleCatalogOut
        ] = SimpleGettingDataFromCatalog[SimpleCatalogOut]()
        self.adding_data: AbstractAddingDataToCatalog[
            SimpleCatalogIn, SimpleCatalogOut
        ] = SimpleAddingDataToCatalog()

    async def add_data(self, params: SimpleCatalogIn) -> SimpleCatalogOut:
        return await self.adding_data.add(
            CatalogType.vehicles, params, SimpleCatalogOut
        )

    async def get_data(self, substring: Optional[str]) -> List[SimpleCatalogOut]:
        return await self.getting_data.get_data(
            CatalogType.vehicles, substring, SimpleCatalogOut
        )