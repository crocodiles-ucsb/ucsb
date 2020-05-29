from datetime import date
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel
from src.database.models import RequestStatus, WorkerInRequestStatus


class TokensResponse(BaseModel):
    token_type: str
    access_token: bytes
    refresh_token: bytes


class InUser(BaseModel):
    username: str
    password: str


class InUserWithUUID(InUser):
    uuid: str


class OutUser(BaseModel):
    id: int
    username: str
    type: str

    class Config:
        orm_mode = True


class MyModel(BaseModel):
    url: str


class UserWithTokens(OutUser):
    access_token: bytes
    refresh_token: bytes


class InRefreshToken(BaseModel):
    refresh_token: str


class OperatorIn(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None


class OperatorOut(OperatorIn):
    class Config:
        orm_mode = True


class SecurityIn(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    position: str


class SecurityOut(SecurityIn):
    class Config:
        orm_mode = True


class SecurityToRegisterOut(SecurityOut):
    uuid: str


class OperatorToRegisterOut(OperatorOut):
    uuid: str


class SimpleCatalogOut(BaseModel):
    id: int
    data: str

    class Config:
        orm_mode = True


class CatalogWithIntValueOut(SimpleCatalogOut):
    value: int


class SimpleCatalogIn(BaseModel):
    data: str


class CatalogWithIntValueIn(SimpleCatalogIn):
    value: int


class SimpleDocumentIn(BaseModel):
    file: UploadFile


class DocumentWithTitleIn(SimpleDocumentIn):
    title: str


class SimpleDocumentOut(BaseModel):
    uuid: str

    class Config:
        orm_mode = True


class DocumentWithTitleOut(SimpleDocumentOut):
    title: str


class ContractorOut(BaseModel):
    id: int
    title: str
    address: str
    ogrn: str
    inn: str

    class Config:
        orm_mode = True


class ContractorRepresentativeOut(BaseModel):
    id: int
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    telephone_number: str
    email: str

    class Config:
        orm_mode = True


class ContractorWithLinksOut(BaseModel):
    id: int
    title: str
    address: str
    ogrn: str
    inn: str
    inn_link: str
    ogrn_link: str


class ContractorInListOut(BaseModel):
    id: int
    title: str
    count_of_workers: int


class WorkerOut(BaseModel):
    id: int
    last_name: str
    first_name: str
    birth_date: date
    contractor_id: int

    class Config:
        orm_mode = True


class WorkerWithProfessionOut(WorkerOut):
    profession: str


class RequestIn(BaseModel):
    object_of_work_id: int
    contract_id: int


class RequestOut(RequestIn):
    id: int
    contractor_id: int
    status: RequestStatus

    class Config:
        orm_mode = True


class RequestInListOut(BaseModel):
    id: int
    contractor_id: int
    title_of_organization: str
    name_of_object: str
    workers_count: int
    contract_link: str
    contract_title: str


class WorkerInRequestOut(BaseModel):
    id: int
    worker_id: int
    request_id: int
    status: WorkerInRequestStatus

    class Config:
        orm_mode = True


class WorkerInRequestIn(BaseModel):
    worker_id: int


class DenyWorkerIn(BaseModel):
    reason_for_rejection_id: int
    comment: Optional[str]
