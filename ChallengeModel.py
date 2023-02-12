from pydantic import BaseModel, Field
from object_id import PyObjectId, ObjectId
from datetime import datetime
from typing import Optional


# create challenge model
class ChallengeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    original_id: Optional[str] = Field(default_factory="")
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    title: str = Field(default_factory="")
    description: str = Field(default_factory="")
    image_url: str = Field(default_factory="https://images.pexels.com/photos/3755440/pexels-photo-3755440.jpeg?auto=compress&cs=tinysrgb&w=600")
    categories: list[str] = Field(default_factory=[])
    duration: int = Field(default_factory=0)
    days: Optional[list[dict]] = Field(default_factory=[])
    joiners: Optional[list[str]] = Field(default_factory=[])

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
