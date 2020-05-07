from src.DAL.registration import (
    AbstractRegistration,
    SimpleRegistration,
    SimpleRegistrationParams,
)
from src.DAL.user import User
from src.models import OutUser


class Admin(User[SimpleRegistrationParams]):
    def __init__(self) -> None:
        self.registration: AbstractRegistration[
            SimpleRegistrationParams
        ] = SimpleRegistration()

    async def register_user(self, params: SimpleRegistrationParams) -> OutUser:
        return await self.registration.register(params)
