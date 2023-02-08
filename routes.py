from models import ChallengeModel, UpdateChallengeModel, ExerciseModel
from main import app, challenges_db, exercises_db
from fastapi import status, HTTPException, Body, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List


# -------------- home page routes --------------- #


@app.get("/")
def success_message():
    return {"message": "Welcome to Thirty Days"}

# ----------- browse page routes ------------ #

# get all challenges


@app.get("/challenges", response_description="List all challenges", response_model=List[ChallengeModel])
async def list_challenges():
    challenges = await challenges_db.find().to_list(1000)
    return challenges


# filter challenges by keyword, category, duration, or all three
@app.get("/challenges", response_description="Filter challenges", response_model=List[ChallengeModel])
async def filter_challenges(keywords: str, categories: list[str], durations: list[int]):
    challenges = await challenges_db.find().to_list(1000)
    filtered_challenges = []
    for challenge in challenges:
        if keywords in challenge["title"] or keywords in challenge['description']:
            filtered_challenges.append(challenge)
    return filtered_challenges


# ----------- challenge page routes ----------- #

# get a single challenge


@app.get("/challenges/{id}", response_description="Get a single challenge", response_model=ChallengeModel)
async def show_challenge(id: str):
    if (challenge := await challenges_db.find_one({"_id": id})) is not None:
        return challenge

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")

# join a challenge


@app.patch("/challenges/{id}/join")
async def join_challenge(id: str):
    challenge = await challenges_db.find_one({"_id": id})
    joiners = challenge["joiners"]
    joiners += 1
    await challenges_db.update_one({"_id": id}, {"$set": {"joiners": joiners}})
    return challenge


# ----------- day page routes ----------- #

# get a single day

@app.get("/challenges/{id}/day/{day}")
async def show_challenge_day(id: str, day: int):
    return db.find_one({"challenge_id": challenge_id, "day": day})

# ----------- excercise page routes ----------- #

# get all excercises


@app.get("/exercises", response_description="List all excercises", response_model=List[ExerciseModel])
async def list_excercises():
    excercises = await exercises_db.find().to_list(10)
    return excercises

# filter excercises by primary/secondary muscle group


@app.get("/exercises", response_description="Filter excercises", response_model=List[ExerciseModel])
async def filter_excercises(muscle: str = Query(None)):
    query = {}
    if muscle:
        query = {"primary": muscle}
    exercises = [x for x in exercises_db.find(query)]
    return exercises

# get a single excercise


@app.get("/exercises/{id}", response_description="Get a single excercise", response_model=ExerciseModel)
async def show_excercise(id: str):
    if (excercise := await exercises_db.find_one({"_id": id})) is not None:
        return excercise

    raise HTTPException(status_code=404, detail=f"Excercise {id} not found")


# -------------- create challenge page routes --------------- #

# create a challenge
@app.post("/challenges", response_description="Create a new challenge", response_model=ChallengeModel)
async def create_challenge(challenge: ChallengeModel = Body(...)):
    challenge = jsonable_encoder(challenge)
    new_challenge = await challenges_db.insert_one(challenge)
    created_challenge = await challenges_db.find_one({"_id": new_challenge.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_challenge)

# update a challenge


@app.put("/challenges/{id}", response_description="Update a challenge", response_model=ChallengeModel)
async def update_challenge(id: str, challenge: UpdateChallengeModel = Body(...)):
    challenge = {k: v for k, v in challenge.dict().items() if v is not None}

    if len(challenge) >= 1:
        update_result = await challenges_db.update_one({"_id": id}, {"$set": challenge})

        if update_result.modified_count == 1:
            if (update_challenge := await challenges_db.find_one({"_id": id})) is not None:
                return update_challenge

    if (existing_challenge := await challenges_db.find_one({"_id": id})) is not None:
        return existing_challenge

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")

# delete a challenge


@app.delete("/challenges/{id}", response_description="Delete a challenge")
async def delete_challenge(id: str):
    delete_result = await challenges_db.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")

# -------------- create day page routes --------------- #

# create a day


# add an excercise to a day


@app.patch("/challenges/{challenge_id}/day/{day_id}")
def add_excercise_to_day(challenge_id: str, day_id: int, excercise: dict):
    return db.update_one({"challenge_id": challenge_id, "day.id": day_id}, {"$push": {"day.excercises": excercise}})

# ------------- dashboard page routes --------------- #

# get all challenges created or joined by user


@app.get("/dashboard")
async def get_user_challenges(user_id):
    created = db.find({"created_by": user_id})
    joined = db.find({"joiners": user_id})

    return {"created": created, "joined": joined}
