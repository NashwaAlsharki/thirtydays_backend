from pydantic import BaseModel, Field
from object_id import PyObjectId
from datetime import datetime

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
        json_encoders = {PyObjectId: str}

class UpdateUserModel(BaseModel):
    email: str
    password: str
    username: str = None
    created_challenges: list[str] = []
    joined_challenges: list[str] = []
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}