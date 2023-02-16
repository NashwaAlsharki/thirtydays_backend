from pydantic import BaseModel, Field
from object_id import PyObjectId, ObjectId
from datetime import datetime
from typing import Optional


# create challenge model
class ChallengeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    original_id: str = ""
    created_by: str = Field(...)
    title: str = ""
    description: str = ""
    image_url: str = "https://images.pexels.com/photos/3755440/pexels-photo-3755440.jpeg?auto=compress&cs=tinysrgb&w=600"
    categories: list[str] = []
    duration: int = 0
    days: list[dict] = [{"number": 1, "description": "", "completed": False, "exercises": []}]
    joiners: list[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateChallengeModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    categories: list[str]
    duration: Optional[int]
    days: Optional[list[dict]]
    joiners: Optional[list[str]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# create copied challenge model
class CopiedChallengeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    joiners: list[str] = []
    original_id: str = Field(...)
    created_by: str = Field(...)
    joined_by: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    image_url: str = Field(...)
    categories: list[str] = Field(...)
    duration: int = Field(...)
    days: list[dict] = Field(...)
    completion_precent: int = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}