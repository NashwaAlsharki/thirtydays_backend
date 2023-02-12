from pydantic import BaseModel, Field, EmailStr
from object_id import PyObjectId, ObjectId
from datetime import datetime
from typing import Optional


# create user model
class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    email: EmailStr = Field(...)
    password: str = Field(...)
    username: str = "Friend"
    created_challenges: list[str] = []
    joined_challenges: list[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateUserModel(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    username: Optional[str]
    created_challenges: Optional[list]
    joined_challenges: Optional[list]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}