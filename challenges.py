from ChallengeModel import ChallengeModel, UpdateChallengeModel
from fastapi import status, HTTPException, Body, APIRouter
from db_connection import users_db, challenges_db
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List


router = APIRouter()

# get all challenges or filter by keyword, category, duration, or all three
@router.get("/challenges", response_description="List challenges", response_model=List[ChallengeModel])
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
@router.get("/challenges/{id}", response_description="Get a single challenge", response_model=ChallengeModel)
async def show_challenge(id: str):
    if (challenge := await challenges_db.find_one({"_id": id})):
        return challenge

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")

# create a challenge and add to user's created challenges
@router.post("/challenge", response_description="Create a new challenge", response_model=ChallengeModel)
async def create_challenge(challenge: ChallengeModel = Body(...)):
    challenge = jsonable_encoder(challenge)
    new_challenge = await challenges_db.insert_one(challenge)
    challenge_id = new_challenge.inserted_id
    update_challenge = await challenges_db.update_one({"_id": challenge_id}, {"$set": {"original_id": challenge_id}})
    if (await users_db.update_one({"_id": challenge["creator"]}, {"$push": {"createdChallenges": challenge_id}})):
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_challenge)

    raise HTTPException(status_code=500, detail="Something went wrong")

# update a challenge
@router.put("/challenges/{id}", response_description="Update a challenge", response_model=ChallengeModel)
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
@router.delete("/challenges/{id}", response_description="Delete a challenge")
async def delete_challenge(id: str):
    delete_result = await challenges_db.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")