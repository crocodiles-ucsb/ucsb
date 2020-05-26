from dataclasses import dataclass
from http import HTTPStatus
from io import StringIO
from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from src.api.catalogs import CatalogType
from src.database.models import (
    Admin,
    AnotherDriveLicense,
    Catalog,
    CertificateOfCompetency,
    ContractorRepresentative,
    ContractorRepresentativeToRegister,
    Document,
    DrivingLicense,
    EmergencyDrivingCertificate,
    Identification,
    Inn,
    InstructedInformation,
    MedicalCertificate,
    ObjectOfWork,
    Ogrn,
    Operator,
    OperatorToRegister,
    OrderOfAcceptanceToWork,
    Profession,
    ReasonForRejectionOfApplication,
    Security,
    SecurityToRegister,
    SpecialityCourseInformation,
    TrainingInformation,
    User,
    UserToRegister,
    Vehicle,
    Violation,
)
from src.database.user_roles import UserRole
from src.exceptions import DALError
from src.messages import Message
from src.models import DocumentWithTitleOut, OutUser, SimpleDocumentOut
from src.urls import Urls


def get_url_postfix(user: OutUser) -> str:
    res = StringIO()
    res.write('/')
    if user.type == UserRole.SECURITY.value:
        res.write(user.type[:-1])
        res.write('ies')
    else:
        res.write(user.type)
        res.write('s')
    return res.getvalue()


def get_registration_url(uuid: str) -> str:
    return f'{Urls.registration_url}/{uuid}'


def get_db_obj(user_role: UserRole) -> Type[User]:
    if user_role == UserRole.ADMIN:
        return Admin
    if user_role == UserRole.OPERATOR:
        return Operator
    if user_role == UserRole.CONTRACTOR_REPRESENTATIVE:
        return ContractorRepresentative
    if user_role == UserRole.SECURITY:
        return Security
    raise ValueError()


def get_obj_from_obj_to_register(user_to_register: UserToRegister) -> Type[User]:
    if isinstance(user_to_register, OperatorToRegister):
        return Operator
    if isinstance(user_to_register, SecurityToRegister):
        return Security
    raise ValueError()


def get_db_obj_to_register(user_role: UserRole) -> Type[UserToRegister]:
    if user_role == UserRole.OPERATOR:
        return OperatorToRegister
    if user_role == UserRole.SECURITY:
        return SecurityToRegister
    if user_role == UserRole.CONTRACTOR_REPRESENTATIVE:
        return ContractorRepresentativeToRegister
    raise ValueError()


T = TypeVar('T')


@dataclass(init=False)
class Pagination:
    has_next_page: bool = False
    has_prev_page: bool = False
    current_page: int = 1
    prev_page: Optional[int] = None
    next_page: Optional[int] = None


class ListWithPagination(Generic[T]):
    def __init__(self, data: List[T], pagination_params: Pagination):
        self.data: List[T] = data
        self.pagination_params: Pagination = pagination_params


def get_pagination(objects: List[T], page: int, size: int) -> ListWithPagination[T]:
    pagination = Pagination()
    start_index: int = 0
    catch_error(objects, page, size)
    pagination.current_page = page
    if page > 1:
        start_index = (page - 1) * size
        pagination.has_prev_page = True
        pagination.prev_page = page - 1
    end_index: int = start_index + size - 1
    length = len(objects)
    if end_index >= length:
        end_index = length - 1
    if end_index < length - 1:
        pagination.has_next_page = True
        pagination.next_page = page + 1
    res: List[T] = []
    for i in range(start_index, end_index + 1):
        res.append(objects[i])

    return ListWithPagination(res, pagination)


def catch_error(objects, page, size):
    if page < 1 or size < 1 or page * size > len(objects) + size:
        raise DALError(
            HTTPStatus.BAD_REQUEST.value, Message.INVALID_PAGINATION_PARAMS.value
        )


def get_catalog_db_obj(catalog_type: CatalogType) -> Type[Catalog]:
    if catalog_type == CatalogType.professions:
        return Profession
    if catalog_type == CatalogType.objects_of_work:
        return ObjectOfWork
    if catalog_type == CatalogType.vehicles:
        return Vehicle
    if catalog_type == CatalogType.reasons_for_rejection_of_application:
        return ReasonForRejectionOfApplication
    if catalog_type == CatalogType.violations:
        return Violation
    raise ValueError()


def get_document_out_model(document_type: str) -> Type[BaseModel]:
    if document_type == 'contract':
        return DocumentWithTitleOut
    return SimpleDocumentOut


def get_document_db_type(type: str) -> Type[Document]:
    if type == 'identification':
        return Identification
    if type == 'driving_license':
        return DrivingLicense
    if type == 'order_of_acceptance_to_work':
        return OrderOfAcceptanceToWork
    if type == 'training_information':
        return TrainingInformation
    if type == 'speciality_course_information':
        return SpecialityCourseInformation
    if type == 'another_drive_license':
        return AnotherDriveLicense
    if type == 'medical_certificate':
        return MedicalCertificate
    if type == 'certificate_of_competency':
        return CertificateOfCompetency
    if type == 'instructed_information':
        return InstructedInformation
    if type == 'emergency_driving_certificate':
        return EmergencyDrivingCertificate
    if type == 'ogrn_document':
        return Ogrn
    if type == 'inn_document':
        return Inn
    raise ValueError()
