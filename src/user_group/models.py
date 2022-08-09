from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.core.models import CreateInfoMixIn
from src.db.base_class import Base

if TYPE_CHECKING:
    from src.user.models import User


class PermissionCategory(CreateInfoMixIn):
    id = Column(None, ForeignKey('createinfomixin.id'), primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)


class CustomPermission(CreateInfoMixIn):
    id = Column(None, ForeignKey('createinfomixin.id'), primary_key=True, index=True, autoincrement=True)
    code_name = Column(String(50), index=True, nullable=False)
    category_id = Column(ForeignKey("permissioncategory.id"), nullable=True)


class CustomGroup(CreateInfoMixIn):
    id = Column(None, ForeignKey('createinfomixin.id'), primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)
    permissions = relationship("CustomPermission", backref="groups")
    user = relationship("User",
                        secondary='usergrouprelation',
                        back_populates="groups", cascade="all, delete")
