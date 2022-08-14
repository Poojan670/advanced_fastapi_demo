import re

from pydantic_choices import choice
from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr, Field, validator
from datetime import date

gender_choices = choice(
    ["Male",
     "Female",
     "Others"]
)


# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


# Retrieve User
class ShowUser(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserCreate(BaseModel):
    username: constr(min_length=3,
                     max_length=10,
                     to_lower=True)
    email: EmailStr
    password: str = Field(..., min_length=5,
                          max_length=15)


# Properties to receive via API on update
class ChangePassword(BaseModel):
    new_password: str = Field(..., min_length=5, max_length=15)
    confirm_password: Optional[str] = None

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    username: Optional[constr(min_length=3,
                              max_length=10,
                              to_lower=True)] = None
    email: Optional[EmailStr] = None


class UserInDBBase(BaseModel):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


# Msg Schemas
class Message(BaseModel):
    msg: str


# User Details

class UserDetailsBase(BaseModel):
    first_name: constr(min_length=3, max_length=20)
    middle_name: Optional[str] = None
    last_name: constr(min_length=3, max_length=20)
    birthday: date
    gender: gender_choices
    phone: constr(min_length=10, max_length=15)

    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v
