import sqlalchemy as sa
from src.database.database import Base


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True)
    password_hash = sa.Column(sa.String)
    access_token = sa.Column(sa.String)
    refresh_token = sa.Column(sa.String)
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
    last_name = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String, nullable=False)
    patronymic = sa.Column(sa.String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'operator',
    }


class Security(User):
    __tablename__ = 'security'
    id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'security',
    }


class ContractorRepresentative(User):
    __tablename__ = 'contractor_representative'
    id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'contractor_representative',
    }


class UserToRegister(Base):
    __tablename__ = 'user_to_register'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    uuid = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'user_to_register',
        'polymorphic_on': type,
    }


class OperatorToRegister(UserToRegister):
    __tablename__ = 'operator_to_register'
    id = sa.Column(sa.Integer, sa.ForeignKey('user_to_register.id'), primary_key=True)
    last_name = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String, nullable=False)
    patronymic = sa.Column(sa.String, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'operator_to_register',
    }


class SecurityToRegister(UserToRegister):
    __tablename__ = 'security_to_register'
    id = sa.Column(sa.Integer, sa.ForeignKey('user_to_register.id'), primary_key=True)
    last_name = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String, nullable=False)
    patronymic = sa.Column(sa.String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'security_to_register',
    }


class ContractorRepresentativeToRegister(UserToRegister):
    __tablename__ = 'contractor_representative_to_register'
    id = sa.Column(sa.Integer, sa.ForeignKey('user_to_register.id'), primary_key=True)
    last_name = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String, nullable=False)
    patronymic = sa.Column(sa.String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'contractor_representative_to_register',
    }
