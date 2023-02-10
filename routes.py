from models import UserModel, UpdateUserModel, ChallengeModel, UpdateChallengeModel, ExerciseModel
from main import app, users_db, challenges_db, exercises_db
from fastapi import status, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List


# -------------- home page routes --------------- #
@app.get("/")
def success_message():
    return {"message": "Welcome to Thirty Days"}

# -------------- user routes --------------- #

# signup a new user
@app.post("/signup", response_description="Signup a new user", response_model=UserModel)
async def signup_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await users_db.insert_one(user)
    created_user = await users_db.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

# login a user
@app.post("/login", response_description="Login a user", response_model=UserModel)
async def login_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    if (found_user := await users_db.find_one({"email": user["email"]})):
        if found_user["password"] == user["password"]:
            return found_user
        raise HTTPException(status_code=404, detail="Incorrect password")
    raise HTTPException(status_code=404, detail="User not found")

# ----------- challenge routes ----------- #

# get all challenges or filter by keyword, category, duration, or all three


@app.get("/challenges", response_description="List challenges", response_model=List[ChallengeModel])
async def list_challenges(keywords: str = None, duration: int = None, category: str = None):
    query = {}
    if keywords:
        query = {"$or": [{"title": {"$regex": keyword, "$options": "i"}}, {
            "description": {"$regex": keyword, "$options": "i"}}]}
    if duration:
        query["duration"] = duration
    if category:
        query["categories"] = {"$in": [category]}

    if (challenges := await challenges_db.find(query).to_list(1000)):
        return challenges

    raise HTTPException(status_code=404, detail="No challenges found")

# get a single challenge


@app.get("/challenges/{id}", response_description="Get a single challenge", response_model=ChallengeModel)
async def show_challenge(id: str):
    if (challenge := await challenges_db.find_one({"_id": id})):
        return challenge

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")

# add user to challenge joiners, add challenge to user joined challenges
@app.patch("/challenges/{id}/join/{user_id}")
async def join_challenge(id: str, user_id: str):
    if (await challenges_db.update_one({"_id": id}, {"$inc": {"joiners": 1}})):
        if (await users_db.update_one({"_id": user_id}, {"$push": {"joinedChallenges": id}})):
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Joined challenge successfully"})





@app.patch("/challenges/{id}/join")
async def join_challenge(id: str):
    if (await challenges_db.update_one({"_id": id}, {"$inc": {"joiners": 1}})):
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Joined challenge successfully"})

    raise HTTPException(status_code=500, detail="Something went wrong")

# create a challenge


@app.post("/challenges", response_description="Create a new challenge", response_model=ChallengeModel)
async def create_challenge(challenge: ChallengeModel = Body(...)):
    challenge = jsonable_encoder(challenge)
    new_challenge = await challenges_db.insert_one(challenge)

    if (challenge_id := await challenges_db.find_one({"_id": new_challenge.inserted_id})):
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=challenge_id)

    raise HTTPException(status_code=500, detail="Something went wrong")

# update a challenge


@app.put("/challenges/{id}", response_description="Update a challenge", response_model=ChallengeModel)
async def update_challenge(id: str, challenge: UpdateChallengeModel = Body(...)):
    challenge = {k: v for k, v in challenge.dict().items() if v}

    if len(challenge) >= 1:
        update_result = await challenges_db.update_one({"_id": id}, {"$set": challenge})

        if update_result.modified_count == 1:
            if (update_challenge := await challenges_db.find_one({"_id": id})):
                return update_challenge

    if (existing_challenge := await challenges_db.find_one({"_id": id})):
        return existing_challenge

    raise HTTPException(status_code=500, detail="Something went wrong")

# delete a challenge


@app.delete("/challenges/{id}", response_description="Delete a challenge")
async def delete_challenge(id: str):
    delete_result = await challenges_db.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")

# ----------- excercise routes ----------- #

# get all excercises with filters for primary and secondary muscle groups


@app.get("/exercises", response_description="Filter excercises", response_model=List[ExerciseModel])
async def filter_excercises(muscle: str = None):
    query = {}
    if muscle:
        query = {"$or": [{"primary": muscle},
                         {"secondary": {"$in": [muscle]}}]}

    if (excercises := await exercises_db.find(query).to_list(1000)):
        return excercises

    raise HTTPException(status_code=404, detail="No excercises found")

# get one excercise


@app.get("/exercises/{id}", response_description="Get a single excercise", response_model=ExerciseModel)
async def show_excercise(id: str):
    if (excercise := await exercises_db.find_one({"_id": id})):
        return excercise

    raise HTTPException(status_code=404, detail=f"Excercise {id} not found")

# --------------  day  routes --------------- #

# create a day


@app.patch("/challenges/{id}/day", response_description="Create a new day")
async def create_day(id: str, day: dict):
    challenge = await challenges_db.find_one({"_id": id})
    day = jsonable_encoder(day)
    day["_id"] = len(challenge["days"]) + 1
    # add day to challenge and increment challenge duration
    update_challenge = await challenges_db.update_one({"_id": id}, {"$push": {"days": day}, "$inc": {"duration": 1}})
    if update_challenge.modified_count > 0:
        return {"message": "Day added successfully"}

    raise HTTPException(status_code=500, detail="An error occurred")

# get a day


@app.get("/challenges/{id}/day/{day_id}", response_description="Get a single day")
async def show_day(id: str, day_id: int):
    challenge = await challenges_db.find_one({"_id": id})
    for day in challenge["days"]:
        if day["_id"] == day_id:
            return day

    raise HTTPException(status_code=500, detail="An error occurred")

# delete a day


@app.delete("/challenges/{id}/day/{day_id}", response_description="Delete a day")
async def delete_day(id: str, day_id: int):
    challenge = await challenges_db.find_one({"_id": id})
    for day in challenge["days"]:
        if day["_id"] == day_id:
            update_challenge = await challenges_db.update_one({"_id": id}, {"$pull": {"days": day}})
            if update_challenge.modified_count == 1:
                return {"message": "Day deleted successfully"}
