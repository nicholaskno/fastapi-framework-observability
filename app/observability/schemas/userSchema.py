from pydantic import BaseModel, EmailStr, Field, constr
from datetime import datetime
from typing import Optional, List, Literal
from uuid import UUID


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class MessageResponse(BaseModel):
    message: str

class UserInfo(BaseModel):
    id: str
    name: str
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    user: UserInfo
