from pydantic import BaseModel, Field
from object_id import PyObjectId
from datetime import datetime


# create challenge model
class ChallengeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    original_id: str
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    title: str
    description: str
    image_url: str
    categories: list[str]
    duration: int
    days: list
    joiners: list[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class UpdateChallengeModel(BaseModel):
    title: str
    description: str
    image_url: str
    categories: list[str]
    duration: int
    days: list
    joiners: list[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
