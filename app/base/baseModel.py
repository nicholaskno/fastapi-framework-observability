from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
import uuid


Base = declarative_base()

#TO-DO: Threatment for table name generation when name has underscore
class TableNameMixin:
    @declared_attr
    def __tablename__(cls):
        module_prefix = cls.__module__.split('.')[-3]
        return f"{module_prefix}_{cls.__name__.lower()}"
    

class BaseModel(Base, TableNameMixin):
    __abstract__ = True  # This is an abstract base class, that means it won't be created as a table in the database

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_insert = Column(DateTime(timezone=True), default=func.now())
    date_last_update = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

