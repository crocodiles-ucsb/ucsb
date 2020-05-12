from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from src.DAL.users.user import User

TAddingUserParams = TypeVar('TAddingUserParams', bound=Any)
TAddingUserOut = TypeVar('TAddingUserOut', bound=BaseModel)


class SimpleUser(Generic[TAddingUserParams, TAddingUserOut], User, ABC):
    @abstractmethod
    async def add_user(self, params: TAddingUserParams) -> TAddingUserOut:
        pass
