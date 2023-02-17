from ..models.ChallengeModel import ChallengeModel, UpdateChallengeModel, CopiedChallengeModel
from fastapi import status, HTTPException, APIRouter
from ..db_connection import users_db, challenges_db
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List

router = APIRouter()

# get all challenges or filter by keyword, category, duration, or all three
@router.get("/challenges", response_model=List[ChallengeModel])
async def list_challenges(keywords: str = None, duration: int = None, category: str = None):
    query = {"original_id": ""}
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
@router.get("/challenges/{id}", response_model=ChallengeModel)
async def show_challenge(id: str):
    if (challenge := await challenges_db.find_one({"_id": id})):
        return challenge

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")

# create a challenge and add to user's created challenges
@router.post("/challenges", response_model=ChallengeModel)
async def create_challenge(challenge: ChallengeModel):
    challenge = jsonable_encoder(challenge)
    new_challenge = await challenges_db.insert_one(challenge)
    
    created_challenge = await challenges_db.find_one({"_id": new_challenge.inserted_id})
        
    await users_db.update_one({"_id": challenge["created_by"]}, {"$push": {"created_challenges": created_challenge["_id"]}})
        
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_challenge)
    
# add user to challenge joiners
@router.patch("/challenges/{id}/join/{user_id}")
async def join_challenge(id: str, user_id: str):
    challenge = await challenges_db.find_one({"_id": id})
    
    if user_id in challenge["joiners"]:
        raise HTTPException(status_code=400, detail="You have already joined this challenge")

    # add user to challenge joiners
    await challenges_db.update_one({"_id": id}, {"$push": {"joiners": user_id}})
    
    # copy challenge and add to user's joined challenges
    duplicate_challenge = CopiedChallengeModel (
        original_id = challenge["_id"],
        created_by = challenge["created_by"],
        joined_by = user_id,
        joiners = challenge["joiners"],
        title = challenge["title"],
        description = challenge["description"],
        duration = challenge["duration"],
        categories = challenge["categories"],
        image_url = challenge["image_url"],
        days = challenge["days"],
    )

    duplicate_challenge = jsonable_encoder(duplicate_challenge)
    
    user_copy = await challenges_db.insert_one(duplicate_challenge)
    await users_db.update_one({"_id": user_id}, {"$push": {"joined_challenges": user_copy.inserted_id}})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Joined challenge successfully"})

# update a challenge (not properly tested)
@router.put("/challenges/{id}", response_model=ChallengeModel)
async def update_challenge(id: str, challenge: UpdateChallengeModel):
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