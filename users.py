from UserModel import UserModel, UpdateUserModel
from db_connection import users_db, challenges_db
from fastapi import status, HTTPException, Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

# signup a new user
@router.post("/users/signup", response_description="Signup a new user", response_model=UserModel)
async def signup_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    if (found_user := await users_db.find_one({"email": user["email"]})):
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        new_user = await users_db.insert_one(user)
    if (created_user := await users_db.find_one({"_id": new_user.inserted_id})):
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

    raise HTTPException(status_code=500, detail="Something went wrong")

# login a user
@router.post("/users/login", response_description="Login a user", response_model=UserModel)
async def login_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    if (found_user := await users_db.find_one({"email": user["email"]})):
        if found_user["password"] == user["password"]:
            return found_user
        raise HTTPException(status_code=404, detail="Incorrect password")
    raise HTTPException(status_code=404, detail="User not found")

# update user details
@router.put("/users/{id}", response_description="Update user details", response_model=UpdateUserModel)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    if (await users_db.update_one({"_id": id}, {"$set": user.dict()})):
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User updated successfully"})
    
    raise HTTPException(status_code=500, detail="Something went wrong")

# add challenge to user joined challenges
@router.patch("/challenges/{id}/join/{user_id}", response_description="Join a challenge")
async def join_challenge(id: str, user_id: str):
    challenge = challenges_db.update_one({"_id": id}, {"$push": {"joiners": user_id}})
    copied_challenge = challenge.copy()
    if (added_challenge := await users_db.update_one({"_id": user_id}, {"$push": {"joinedChallenges": copied_challenge["_id"]}})):
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Joined challenge successfully"})

    raise HTTPException(status_code=500, detail="Something went wrong")