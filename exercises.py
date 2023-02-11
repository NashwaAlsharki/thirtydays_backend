from ExerciseModel import ExerciseModel
from fastapi import status, HTTPException, Body, APIRouter
from db_connection import exercises_db
from typing import List

router = APIRouter()

# get all excercises with filters for primary and secondary muscle groups
@router.get("/exercises", response_description="Filter excercises", response_model=List[ExerciseModel])
async def filter_excercises(muscle: str = None):
    query = {}
    if muscle:
        query = {"$or": [{"primary": muscle},
                         {"secondary": {"$in": [muscle]}}]}

    if (excercises := await exercises_db.find(query).to_list(1000)):
        return excercises

    raise HTTPException(status_code=404, detail="No excercises found")

# get one excercise
@router.get("/exercises/{id}", response_description="Get a single excercise", response_model=ExerciseModel)
async def show_excercise(id: str):
    if (excercise := await exercises_db.find_one({"_id": id})):
        return excercise

    raise HTTPException(status_code=404, detail=f"Excercise {id} not found")