from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from ..app import PyObjectId

class TreeDiagram(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    model_data: dict
    users: list[str]

class User(BaseModel):
    """
    Container for a single user record.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    user_id: str = Field(...)