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
    patronymic: str = ''


class OperatorOut(OperatorIn):
    class Config:
        orm_mode = True


class SecurityIn(BaseModel):
    first_name: str
    last_name: str
    patronymic: str = ''
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
    id: int
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
    patronymic: str = ''
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


class RequestForTemplateOut(BaseModel):
    id: int
    contractor_id: int
    title_of_organization: str
    name_of_object: str
    workers_count: int
    contract_link: str
    contract_title: str
    status: RequestStatus


class WorkerInRequestOut(BaseModel):
    id: int
    worker_id: int
    request_id: int
    status: WorkerInRequestStatus

    class Config:
        orm_mode = True


class WorkerInRequestIn(BaseModel):
    worker_id: int


class WorkerInListOut(BaseModel):
    last_name: str
    first_name: str
    patronymic: str = ''
    id: int
    profession: str
    penalty_points: int
    status: WorkerInRequestStatus
    reason_of_rejection: Optional[str]


class DenyWorkerIn(BaseModel):
    reason_for_rejection_id: int
    comment: Optional[str]


class WorkerSimpleOut(BaseModel):
    id: int
    last_name: str
    first_name: str
    patronymic: str
    profession: str
    birth_date: date
    violations_points: int


class WorkerSimpleOutWithRequestInfo(WorkerSimpleOut):
    status: WorkerInRequestStatus
    comment: str
    reason: str


class WorkerComplexOut(BaseModel):
    id: int
    last_name: str
    first_name: str
    patronymic: str
    profession: str
    birth_date: date
    identification_uuid: str
    driving_license_uuid: Optional[str]
    order_of_acceptance_to_work_uuid: Optional[str]
    training_information_uuid: Optional[str]
    speciality_course_information_uuid: Optional[str]
    another_drive_license_uuid: Optional[str]
    medical_certificate_uuid: Optional[str]
    certificate_of_competency_uuid: Optional[str]
    instructed_information_uuid: Optional[str]
    emergency_driving_certificate_uuid: Optional[str]
    violations_points: int
    count_of_violations: int


class ObjectOut(BaseModel):
    data: str
