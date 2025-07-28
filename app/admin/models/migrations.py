from sqlalchemy import Column, String
from app.base.baseModel import Base, BaseModel


class Migrations(BaseModel):
    name = Column(String(100), unique=True)
    