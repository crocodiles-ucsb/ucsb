import sqlalchemy as sa
from src.database.database import Base


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True)
    user_type = sa.Column(sa.Enum, nullable=False)
    password_hash = sa.Column(sa.String)
    access_token = sa.Column(sa.String)
    refresh_token = sa.Column(sa.String)
