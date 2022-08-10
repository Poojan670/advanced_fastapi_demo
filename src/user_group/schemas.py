from typing import List

from pydantic import (
    BaseModel, Field
)


class PermissionCategory(BaseModel):
    name: Field(default=None, max_length=50, example="User")

    class Config:
        schema_extra = {
            "example": {
                "name": "User"
            }
        }


class CustomPermission(BaseModel):
    name = Field(default=None, max_length=50, example="Can Add Users")
    code_name = Field(default=None, max_length=50, example="can_add_user")
    category = int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Can Add User",
                "code_name": "can_add_user",
                "category": "1"
            }
        }


class CustomGroup(BaseModel):
    name: Field(default=None, max_length=50, example="Manager")
    permissions = List[CustomPermission]
    is_active: bool
    remarks: Field(..., max_length=50, example="Remarks for group")

    class Config:
        orm_mode = True
