from models import ChallengeModel, UpdateChallengeModel, ExcerciseModel
from fastapi import FastAPI, status, HTTPException, Body
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from typing import List
import os

# ---------- connect to mongo database ---------- #
load_dotenv()
MONGODB_URI = os.environ.get('MONGODB_URI')
client = AsyncIOMotorClient(MONGODB_URI)
db = client.ThirtyDays


# ---------- create FASTAPI app ---------- #
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------- home page routes --------------- #

@app.get("/")
def success_message():
    return {"message": "Welcome to Thirty Days"}

# ----------- browse page routes ------------ #

# get all challenges

@app.get("/challenges", response_description="List all challenges", response_model=List[ChallengeModel])
async def list_challenges():
    challenges = await db["Challenges"].find().to_list(1000)
    return challenges

# ----------- challenge page routes ----------- #

@app.get("/challenge/{id}", response_description="Get a single challenge", response_model=ChallengeModel)
async def show_challenge(id: str):
    if (challenge := await db["Challenges"].find_one({"_id": id})) is not None:
        return challenge

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")


@app.patch("/challenge/{id}/join")
async def join_challenge(id: str):
    challenge = await db["Challenges"].find_one({"_id": id})
    joiners = challenge["joiners"]
    joiners += 1
    await db["Challenges"].update_one({"_id": id}, {"$set": {"joiners": joiners}})
    return challenge


# ----------- day page routes ----------- #

@app.get("/challenge/{id}/day/{day}")
async def get_challenge_day(id: str, day: int):
    return db.find_one({"challenge_id": challenge_id, "day": day})

# ----------- excercise page routes ----------- #

@app.get("/excercise/{id}", response_description="Get a single excercise", response_model=ExcerciseModel)
async def show_excercise(id: str):
    return db.find_one({"_id": id})


# -------------- create challenge page routes --------------- #


@app.post("/challenge", response_description="Create a new challenge", response_model=ChallengeModel)
async def create_challenge(challenge: ChallengeModel = Body(...)):
    challenge = jsonable_encoder(challenge)
    new_challenge = await db["Challenges"].insert_one(challenge)
    created_challenge = await db["Challenges"].find_one({"_id": new_challenge.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_challenge)

@app.put("/challenge/{id}", response_description="Update a challenge", response_model=ChallengeModel)
async def update_challenge(id: str, challenge: UpdateChallengeModel = Body(...)):
    challenge = {k: v for k, v in challenge.dict().items() if v is not None}

    if len(challenge) >= 1:
        update_result = await db["Challenges"].update_one({"_id": id}, {"$set": challenge})

        if update_result.modified_count == 1:
            if (update_challenge := await db['Challenges'].find_one({"_id": id})) is not None:
                return update_challenge
                
    if (existing_challenge := await db["Challenges"].find_one({"_id": id})) is not None:
        return existing_challenge
    
    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")


@app.delete("/challenge/{id}", response_description="Delete a challenge")
async def delete_challenge(id: str):
    delete_result = await db["Challenges"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")


@app.patch("/challenge/{challenge_id}/day/{day_id}")
async def save_challenge_day(challenge_id: str, day_id: int, day: dict):
    return db.update_one({"challenge_id": challenge_id, "day.id": day_id}, {"$set": day})


@app.patch("/challenge/{challenge_id}/day/{day_id}")
def add_excercise_to_day(challenge_id: str, day_id: int, excercise: dict):
    return db.update_one({"challenge_id": challenge_id, "day.id": day_id}, {"$push": {"day.excercises": excercise}})

# ------------- dashboard page routes --------------- #


@app.get("/dashboard")
async def get_user_challenges(user_id):
    created = db.find({"created_by": user_id})
    joined = db.find({"joiners": user_id})

    return {"created": created, "joined": joined}