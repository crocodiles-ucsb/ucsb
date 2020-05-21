from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

TOutData = TypeVar('TOutData')
TAddData = TypeVar('TAddData')


class AbstractCatalog(Generic[TOutData, TAddData], ABC):
    @abstractmethod
    async def get_data(self, substring: Optional[str]) -> List[TOutData]:
        pass

    @abstractmethod
    async def add_data(self, param: TAddData) -> TOutData:
        pass
