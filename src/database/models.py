from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from src.database.database import Base

association_table_worker_object_of_work = sa.Table(
    'worker_object_of_work_association',
    Base.metadata,
    sa.Column('worker.id', sa.Integer, sa.ForeignKey('object_of_work.id')),
    sa.Column('object_of_work.id', sa.Integer, sa.ForeignKey('worker.id')),
)


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True)
    password_hash = sa.Column(sa.String)
    access_token = sa.Column(sa.String)
    refresh_token = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    first_name = sa.Column(sa.String)
    patronymic = sa.Column(sa.String)
    type = sa.Column(sa.String(50))
    __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': type}


class Admin(User):
    __tablename__ = 'admin'
    id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }


class Operator(User):
    __tablename__ = 'operator'
    id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'operator',
    }


class Security(User):
    __tablename__ = 'security'
    id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    position = sa.Column(sa.String)
    __mapper_args__ = {
        'polymorphic_identity': 'security',
    }


class ContractorRepresentative(User):
    __tablename__ = 'contractor_representative'
    id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    contractor_id = sa.Column(sa.ForeignKey('contractor.id'))

    contractor = relationship('Contractor', back_populates='representatives')
    telephone_number = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'contractor_representative',
    }


class UserToRegister(Base):
    __tablename__ = 'user_to_register'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    uuid = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String(50))
    last_name = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String, nullable=False)
    patronymic = sa.Column(sa.String, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'user_to_register',
        'polymorphic_on': type,
    }


class OperatorToRegister(UserToRegister):
    __tablename__ = 'operator_to_register'
    id = sa.Column(sa.Integer, sa.ForeignKey('user_to_register.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'operator_to_register',
    }


class SecurityToRegister(UserToRegister):
    __tablename__ = 'security_to_register'
    id = sa.Column(sa.Integer, sa.ForeignKey('user_to_register.id'), primary_key=True)
    position = sa.Column(sa.String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'security_to_register',
    }


class ContractorRepresentativeToRegister(UserToRegister):
    __tablename__ = 'contractor_representative_to_register'
    id = sa.Column(sa.Integer, sa.ForeignKey('user_to_register.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'contractor_representative_to_register',
    }


class Catalog(Base):
    __tablename__ = 'catalog'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    type = sa.Column(sa.String(50))
    data = sa.Column(sa.String, nullable=False, unique=True)
    __mapper_args__ = {
        'polymorphic_identity': 'catalog',
        'polymorphic_on': type,
    }


class Profession(Catalog):
    __tablename__ = 'profession'
    id = sa.Column(sa.Integer, sa.ForeignKey('catalog.id'), primary_key=True)

    workers = relationship('Worker', back_populates='profession')
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class Vehicle(Catalog):
    __tablename__ = 'vehicle'
    id = sa.Column(sa.Integer, sa.ForeignKey('catalog.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class ObjectOfWork(Catalog):
    __tablename__ = 'object_of_work'
    id = sa.Column(sa.Integer, sa.ForeignKey('catalog.id'), primary_key=True)

    workers = relationship(
        'Worker',
        secondary=association_table_worker_object_of_work,
        back_populates='objects_of_work',
    )
    requests = relationship('Request', back_populates='object_of_work')
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class ReasonForRejectionOfApplication(Catalog):
    __tablename__ = 'reason_for_rejection_of_application'
    id = sa.Column(sa.Integer, sa.ForeignKey('catalog.id'), primary_key=True)

    workers_requests = relationship(
        'WorkerInRequest', back_populates='reason_for_rejection'
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class Violation(Catalog):
    __tablename__ = 'violation'
    id = sa.Column(sa.Integer, sa.ForeignKey('catalog.id'), primary_key=True)
    value = sa.Column(sa.Integer, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class Document(Base):
    __tablename__ = 'document'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    type = sa.Column(sa.String(50))
    path_to_document = sa.Column(sa.String, nullable=False, unique=True)
    uuid = sa.Column(sa.String)
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type,
    }


class Identification(Document):
    __tablename__ = 'identification'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship('Worker', back_populates='identification', uselist=False)
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class DrivingLicense(Document):
    __tablename__ = 'driving_license'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship('Worker', back_populates='driving_license', uselist=False)
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class OrderOfAcceptanceToWork(Document):
    __tablename__ = 'order_of_acceptance_to_work'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship(
        'Worker', back_populates='order_of_acceptance_to_work', uselist=False
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class TrainingInformation(Document):
    __tablename__ = 'training_information'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship(
        'Worker', back_populates='training_information', uselist=False
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class SpecialityCourseInformation(Document):
    __tablename__ = 'speciality_course_information'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship(
        'Worker', back_populates='speciality_course_information', uselist=False
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AnotherDriveLicense(Document):
    __tablename__ = 'another_drive_license'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship(
        'Worker', back_populates='another_drive_license', uselist=False
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class MedicalCertificate(Document):
    __tablename__ = 'medical_certificate'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship('Worker', back_populates='medical_certificate', uselist=False)
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class CertificateOfCompetency(Document):
    __tablename__ = 'certificate_of_competency'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship(
        'Worker', back_populates='certificate_of_competency', uselist=False
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class InstructedInformation(Document):
    __tablename__ = 'instructed_information'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship(
        'Worker', back_populates='instructed_information', uselist=False
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class EmergencyDrivingCertificate(Document):
    __tablename__ = 'emergency_driving_certificate'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    worker = relationship(
        'Worker', back_populates='emergency_driving_certificate', uselist=False
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class Ogrn(Document):
    __tablename__ = 'ogrn'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    contractor = relationship(
        'Contractor', back_populates='ogrn_document', uselist=False
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class Inn(Document):
    __tablename__ = 'inn'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)

    contractor = relationship(
        'Contractor', back_populates='inn_document', uselist=False
    )
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class Contract(Document):
    __tablename__ = 'contract'
    id = sa.Column(sa.Integer, sa.ForeignKey('document.id'), primary_key=True)
    file_name = sa.Column(sa.String, nullable=False)
    contractor_id = sa.Column(sa.ForeignKey('contractor.id'))

    contractor = relationship('Contractor', back_populates='contracts')
    requests = relationship('Request', back_populates='contract')
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class Worker(Base):
    __tablename__ = 'worker'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    last_name = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String, nullable=False)
    patronymic = sa.Column(sa.String)
    birth_date = sa.Column(sa.Date, nullable=False)
    profession_id = sa.Column(sa.ForeignKey(Profession.id))
    identification_id = sa.Column(sa.ForeignKey(Identification.id))
    driving_license_id = sa.Column(sa.ForeignKey(DrivingLicense.id))
    order_of_acceptance_to_work_id = sa.Column(
        sa.ForeignKey(OrderOfAcceptanceToWork.id)
    )
    training_information_id = sa.Column(sa.ForeignKey(TrainingInformation.id))
    speciality_course_information_id = sa.Column(
        sa.ForeignKey(SpecialityCourseInformation.id)
    )
    another_driver_license_id = sa.Column(sa.ForeignKey(AnotherDriveLicense.id))
    medical_certificate_id = sa.Column(sa.ForeignKey(MedicalCertificate.id))
    certificate_of_competency_id = sa.Column(sa.ForeignKey(CertificateOfCompetency.id))
    instructed_information_id = sa.Column(sa.ForeignKey(InstructedInformation.id))
    emergency_driver_certificate_id = sa.Column(
        sa.ForeignKey(EmergencyDrivingCertificate.id)
    )
    contractor_id = sa.Column(sa.ForeignKey('contractor.id'))

    contractor = relationship('Contractor', back_populates='workers')
    worker_requests = relationship('WorkerInRequest', back_populates='worker')
    objects_of_work = relationship(
        ObjectOfWork,
        secondary=association_table_worker_object_of_work,
        back_populates='workers',
    )
    profession = relationship(Profession, back_populates='workers')
    identification = relationship(Identification, back_populates='worker')
    driving_license = relationship(DrivingLicense, back_populates='worker')
    order_of_acceptance_to_work = relationship(
        OrderOfAcceptanceToWork, back_populates='worker'
    )
    training_information = relationship(TrainingInformation, back_populates='worker')
    speciality_course_information = relationship(
        SpecialityCourseInformation, back_populates='worker'
    )
    another_drive_license = relationship(AnotherDriveLicense, back_populates='worker')
    medical_certificate = relationship(MedicalCertificate, back_populates='worker')
    certificate_of_competency = relationship(
        CertificateOfCompetency, back_populates='worker'
    )
    instructed_information = relationship(
        InstructedInformation, back_populates='worker'
    )
    emergency_driving_certificate = relationship(
        EmergencyDrivingCertificate, back_populates='worker'
    )


class RequestStatus(Enum):
    WAITING_FOR_READINESS = 'waiting for readiness'
    WAITING_FOR_VERIFICATION = 'waiting for verification'
    CLOSED = 'closed'


class Request(Base):
    __tablename__ = 'request'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    object_of_work_id = sa.Column(sa.Integer, sa.ForeignKey(ObjectOfWork.id))
    contract_id = sa.Column(sa.Integer, sa.ForeignKey(Contract.id))
    status = sa.Column(sa.Enum(RequestStatus))

    object_of_work = relationship(ObjectOfWork, back_populates='requests')
    contract = relationship(Contract, back_populates='requests')
    workers_in_request = relationship('WorkerInRequest', back_populates='request')


class WorkerInRequestStatus(Enum):
    WAITING_FOR_READINESS = 'waiting for readiness'
    WAITING_FOR_VERIFICATION = 'waiting for verification'
    ACCEPTED = 'accepted'
    CANCELLED = 'cancelled'


class WorkerInRequest(Base):
    __tablename__ = 'worker_in_request'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    worker_id = sa.Column(sa.ForeignKey(Worker.id))
    request_id = sa.Column(sa.ForeignKey(Request.id), nullable=True)
    status = sa.Column(sa.Enum(WorkerInRequestStatus))
    reason_for_rejection_id = sa.Column(
        sa.ForeignKey(ReasonForRejectionOfApplication.id), nullable=True
    )
    comment = sa.Column(sa.String)

    reason_for_rejection = relationship(
        ReasonForRejectionOfApplication, back_populates='workers_requests'
    )
    worker = relationship(Worker, back_populates='worker_requests')
    request = relationship(Request, back_populates='workers_in_request')


class Contractor(Base):
    __tablename__ = 'contractor'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String, unique=True, nullable=False)
    address = sa.Column(sa.String, nullable=False)
    ogrn = sa.Column(sa.String, nullable=False, unique=True)
    inn = sa.Column(sa.String, nullable=False, unique=True)
    ogrn_document_id = sa.Column(sa.ForeignKey(Ogrn.id))
    inn_document_id = sa.Column(sa.ForeignKey(Inn.id))

    workers = relationship(Worker, back_populates='contractor')
    representatives = relationship(
        ContractorRepresentative, back_populates='contractor'
    )
    ogrn_document = relationship(Ogrn, back_populates='contractor')
    inn_document = relationship(Inn, back_populates='contractor')
    contracts = relationship(Contract, back_populates='contractor')
