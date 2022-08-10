from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.core.models import CreateInfoMixIn
from src.db.base_class import Base

if TYPE_CHECKING:
    pass


class User(CreateInfoMixIn):
    __tablename__ = 'users'
    id = Column(Integer, ForeignKey('createinfomixin.id'), primary_key=True)
    username = Column(String(10), nullable=False, unique=True)
    email = Column(String(20), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    groups = relationship("CustomGroup",
                          secondary='usergrouprelation',
                          back_populates="user", cascade="all, delete")


class UserDetails(CreateInfoMixIn):
    id = Column(Integer, ForeignKey('createinfomixin.id'), primary_key=True)
    first_name = Column(String(20))
    middle_name = Column(String, nullable=True)
    last_name = Column(String(20))
    full_name = Column(String)
    age = Column(Integer)
    birthday = Column(Date)
    gender = Column(String)
    photo = Column(String)
    user = Column(ForeignKey('users.id'), nullable=True)


class UserGroupRelation(Base):
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    group_id = Column(Integer, ForeignKey('customgroup.id'), primary_key=True)
