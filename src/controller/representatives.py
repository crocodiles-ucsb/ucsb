from datetime import datetime

from src.DAL.representatives_dal import RepresentativesDAL


class RepresentativesController:
    @staticmethod
    async def add(
        last_name: str, first_name: str, birthday: datetime, profession: str, **kwargs
    ):
        RepresentativesDAL.add(last_name, first_name, birthday, profession, **kwargs)
