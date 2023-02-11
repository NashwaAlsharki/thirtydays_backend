from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Any, Dict, Type


class PyObjectId(Type[ObjectId]):
    @classmethod
    def __get_validators__(cls) -> Generator:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid object id')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type='string')

# create user model
class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    email: str
    password: str
    username: str = None
    created_challenges: list[str] = []
    joined_challenges: list[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateUserModel(BaseModel):
    email: str
    password: str
    username: str = None
    created_challenges: list[str] = []
    joined_challenges: list[str] = []
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

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
        json_encoders = {ObjectId: str}


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
        json_encoders = {ObjectId: str}
