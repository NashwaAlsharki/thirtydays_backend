from pydantic import BaseModel, Field
from object_id import PyObjectId, ObjectId


# create excercise model
class ExerciseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    primer: str
    style: str
    primary: str
    secondary: list[str]
    equipment: list[str]
    steps: list[str]
    tips: list[str]
    image_urls: list[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}