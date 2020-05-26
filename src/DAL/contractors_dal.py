from http import HTTPStatus
from typing import Awaitable, Optional

from sqlalchemy.exc import IntegrityError
from src.DAL.documents_dal import DocumentsDAL
from src.DAL.utils import ListWithPagination, get_pagination
from src.database.database import create_session, run_in_threadpool
from src.database.models import Contractor
from src.exceptions import DALError
from src.models import ContractorInListOut, ContractorOut, SimpleDocumentIn


class ContractorsDAL:
    @staticmethod
    async def add(
        title: str, address: str, ogrn: str, inn: str, **kwargs
    ) -> ContractorOut:
        with create_session() as session:
            contractor = Contractor(title=title, address=address, ogrn=ogrn, inn=inn)
            session.add(contractor)
            try:
                session.flush()
            except IntegrityError:
                raise DALError(HTTPStatus.BAD_REQUEST.value)
            for key, value in kwargs.items():
                if hasattr(Contractor, key):
                    await DocumentsDAL.add_contractor_document(
                        session, contractor, key, SimpleDocumentIn(file=value)
                    )
            return ContractorOut.from_orm(contractor)

    @staticmethod
    @run_in_threadpool
    def get_all(
        substring: Optional[str], size: int, page: int
    ) -> Awaitable[ListWithPagination[ContractorInListOut]]:
        with create_session() as session:
            contractors = session.query(Contractor).all()
            res = []
            for contractor in contractors:
                if substring and substring not in contractor.title:
                    continue
                count_of_workers: int = len(contractor.workers)
                res.append(
                    ContractorInListOut(
                        id=contractor.id,
                        count_of_workers=count_of_workers,
                        title=contractor.title,
                    )
                )
        return get_pagination(res, page, size)  # type: ignore
