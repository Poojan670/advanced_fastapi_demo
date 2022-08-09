from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from src.db.base_class import Base


class CreateInfoMixIn(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


