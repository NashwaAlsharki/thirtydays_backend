from fastapi import status, HTTPException, APIRouter
from UserModel import UserModel, UpdateUserModel
from ChallengeModel import ChallengeModel, CopiedChallengeModel
from db_connection import users_db, challenges_db
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
import json

router = APIRouter()

# signup a new user
@router.post("/users/signup", response_model= UserModel)
async def signup_user(user: UserModel):
    user = jsonable_encoder(user)

    if (found_user := await users_db.find_one({"email": user["email"]})):
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = await users_db.insert_one(user)
    created_user = await users_db.find_one({"_id": new_user.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
    
# login a user
@router.post("/users/login", response_model=UserModel)
async def login_user(details: dict):
    user = jsonable_encoder(details)
    if (found_user := await users_db.find_one({"email": user["email"]})):
        if (found_user["password"] == user["password"]):
            return JSONResponse(status_code=status.HTTP_200_OK, content=found_user)

        raise HTTPException(status_code=400, detail="Incorrect password")

    raise HTTPException(status_code=404, detail="User not found")

# update user details (not tested)
@router.put("/users/{id}", response_model=UpdateUserModel)
async def update_user(id: str, user: UpdateUserModel):
    user = {k: v for k, v in user.dict().items() if v}
    if len(user) >= 1:
        update_user(id, user)
        if (updated_user := await users_db.find_one({"_id": id})):
            return updated_user


# get user details
@router.get("/users/{id}", response_model=UserModel)
async def get_user(id: str):
    user = await users_db.find_one({"_id": id})
    if user:
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)

    raise HTTPException(status_code=404, detail="User not found")

# get all user created challenges
@router.get("/users/{id}/created_challenges", response_model=ChallengeModel)
async def get_user_challenges(id: str):
    user = await users_db.find_one({"_id": id})
    challenges = []
    for challenge_id in user["created_challenges"]:
        challenge = await challenges_db.find_one({"_id": challenge_id})
        challenges.append(challenge)
    
    if challenges:
        return JSONResponse(status_code=status.HTTP_200_OK, content=challenges)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=[])

# get all user joined challenges
@router.get("/users/{id}/joined_challenges", response_model=CopiedChallengeModel)
async def get_user_joined_challenges(id: str):
    user = await users_db.find_one({"_id": id})
    challenges = []
    for challenge_id in user["joined_challenges"]:
        challenge = await challenges_db.find_one({"_id": challenge_id})
        challenges.append(challenge)
    
    if challenges:
        return JSONResponse(status_code=status.HTTP_200_OK, content=challenges)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=[])

        