from pydantic import BaseModel, Field

# create day model
class DayModel(BaseModel):
    number: int = 1
    description: str = ""
    completed: bool = False
    exercises: list[dict] = [
        { "id": "", "image": "", "title": "", "reps": 0}
    ]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
