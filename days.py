from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, APIRouter
from db_connection import challenges_db

router = APIRouter()

# create a day 
@router.patch("/challenges/{id}/days", response_description="Create a new day")
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
@router.get("/challenges/{id}/days/{day_id}", response_description="Get a single day")
async def show_day(id: str, day_id: int):
    challenge = await challenges_db.find_one({"_id": id})
    for day in challenge["days"]:
        if day["_id"] == day_id:
            return day

    raise HTTPException(status_code=500, detail="An error occurred")

# delete a day
@router.delete("/challenges/{id}/days/{day_id}", response_description="Delete a day")
async def delete_day(id: str, day_id: int):
    challenge = await challenges_db.find_one({"_id": id})
    for day in challenge["days"]:
        if day["_id"] == day_id:
            update_challenge = await challenges_db.update_one({"_id": id}, {"$pull": {"days": day}})
            if update_challenge.modified_count == 1:
                return {"message": "Day deleted successfully"}
