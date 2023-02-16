from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from ExerciseModel import ExerciseModel
from db_connection import exercises_db
from typing import List

router = APIRouter()

# get all excercises with filters for primary and secondary muscle groups
@router.get("/exercises?muscle={muscle}", response_model=List[ExerciseModel])
async def filter_excercises(muscle: str = None):
    query = {}
    if muscle and muscle != "All":
        query = {"$or": [{"primary": {"$regex": muscle, "$options": "i"}},
                         {"secondary": {"$regex": muscle, "$options": "i"}}]}

    if (excercises := await exercises_db.find(query).to_list(20)):
        return JSONResponse(content=excercises)

    raise HTTPException(status_code=404, detail="No excercises found")

# get one excercise
@router.get("/exercises/{exercise_id}" , response_model=ExerciseModel)
async def get_excercise(exercise_id: str):
    exercise = await exercises_db.find_one({"_id": exercise_id})
    return JSONResponse(content=exercise)