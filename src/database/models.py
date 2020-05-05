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
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


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
    __mapper_args__ = {
        'polymorphic_identity': 'security',
    }
