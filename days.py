from db_connection import challenges_db, users_db, exercises_db
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, APIRouter
from DayModel import DayModel

router = APIRouter()

# create a day 
@router.patch("/challenges/{id}/days")
async def create_day(id: str, day: DayModel):
    day = jsonable_encoder(day)
    challenge = await challenges_db.find_one({"_id": id})

    day["number"] = len(challenge["days"]) + 1

    # add day to challenge and increment challenge duration
    update_challenge = await challenges_db.update_one({"_id": id}, {"$push": {"days": day}, "$inc": {"duration": 1}})
    if update_challenge.modified_count > 0:
        return {"message": "Day added successfully"}

    raise HTTPException(status_code=500, detail="An error occurred")

# get a day
@router.get("/challenges/{id}/days/{day_id}", response_model = DayModel)
async def show_day(id: str, day_id: int):
    challenge = await challenges_db.find_one({"_id": id})
    for day in challenge["days"]:
        if day["number"] == day_id:
            return day
        
    raise HTTPException(status_code=404, detail="Day not found")

# get all challenge days
@router.get("/challenges/{id}/days", response_model = list[DayModel])
async def show_days(id: str):
    challenge = await challenges_db.find_one({"_id": id})
    return challenge["days"]

# toggle day completion
@router.patch("/challenges/{id}/days/{day_id}/toggle_complete")
async def toggle_day(id: str, day_id: int):
    challenge = await challenges_db.find_one({"_id": id})
    for day in challenge["days"]:
        if day["number"] == day_id:
            update_day = await challenges_db.update_one({"_id": id, "days.number": day_id}, {"$set": {"days.$.completed": not day["completed"]}, "$set": {"completion_percent": (day["number"] / challenge["duration"]) * 100}})
            
            return {"message": "Day updated successfully"}

    raise HTTPException(status_code=404, detail="Day not found")

# delete a day (not properly tested)
@router.delete("/challenges/{id}/days/{day_id}", response_model = DayModel)
async def delete_day(id: str, day_id: int):
    challenge = await challenges_db.find_one({"_id": id})
    for day in challenge["days"]:
        if day["number"] == day_id:
            update_challenge = await challenges_db.update_one({"_id": id}, {"$pull": {"days": day}})
            if update_challenge.modified_count == 1:
                return {"message": "Day deleted successfully"}