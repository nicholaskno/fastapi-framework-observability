from app.base.baseModel import Base, BaseModel
from sqlalchemy import Column, String, Enum


class User(BaseModel):
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    celphone = Column(String, nullable=True)
    document = Column(String, nullable=True)
    status = Column(Enum('non_confirmed', 'active', 'inactive', name='status_enum'), nullable=False, default='non_confirmed')    
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, status={self.status})>"
    