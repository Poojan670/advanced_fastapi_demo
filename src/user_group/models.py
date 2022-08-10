from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship

from src.core.models import CreateInfoMixIn
from src.db.base_class import Base

if TYPE_CHECKING:
    pass


class PermissionCategory(CreateInfoMixIn):
    id = Column(Integer, ForeignKey('createinfomixin.id'), primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True, unique=True)


class CustomPermission(CreateInfoMixIn):
    id = Column(Integer, ForeignKey('createinfomixin.id'), primary_key=True, index=True)
    code_name = Column(String(50), index=True, nullable=False, unique=True)
    category = Column(ForeignKey("permissioncategory.id"), nullable=True)
    groups = relationship("CustomGroup", secondary="grouppermissionrelation", back_populates="permissions")


class CustomGroup(CreateInfoMixIn):
    id = Column(Integer, ForeignKey('createinfomixin.id'), primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    remarks = Column(String(50), nullable=True)
    is_active = Column(Boolean(), default=False)
    permissions = relationship("CustomPermission",secondary="grouppermissionrelation", back_populates="groups")
    user = relationship("User",
                        secondary='usergrouprelation',
                        back_populates="groups", cascade="all, delete")


class GroupPermissionRelation(Base):
    permission_id = Column(Integer, ForeignKey('custompermission.id'), primary_key=True)

    group_id = Column(Integer, ForeignKey('customgroup.id'), primary_key=True)
