from fastapi import status, HTTPException, APIRouter
from UserModel import UserModel, UpdateUserModel
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


# get user details
@router.get("/users/{id}", response_model=UserModel)
async def get_user(id: str):
    user = await users_db.find_one({"_id": id})
    if user:
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)

    raise HTTPException(status_code=404, detail="User not found")

# add challenge to user joined challenges
@router.patch("/challenges/{id}/join/{user_id}")
async def join_challenge(id: str, user_id: str):
    challenge = challenges_db.update_one(
        {"_id": id}, {"$push": {"joiners": user_id}})
    
    copied_challenge = challenge.copy()
    if (added_challenge := await users_db.update_one({"_id": user_id}, {"$push": {"joinedChallenges": copied_challenge["_id"]}})):
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Joined challenge successfully"})

    raise HTTPException(status_code=500, detail="Something went wrong")
