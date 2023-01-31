from dotenv import load_dotenv
from fastapi import FastAPI
import pymongo
import os

app = FastAPI()

# connect to mongo database
load_dotenv()
DATABASE_URI = os.environ.get('DATABASE_URI')
client = pymongo.MongoClient(DATABASE_URI)
db = client['ThirtyDays']['Challenges']

# ----------------------------------------- #
# home page


@app.get("/")
async def get_featured_challenges():
    # get the 3 challenges with the most joiners
    return db.find().sort("joiners", -1).limit(3)

# ----------------------------------------- #
# browse page


@app.get("/browse")
async def get_challenges(keyword: str, category: str, duration: int):
    # check if any of the filters are applied then query filters
    query = {}
    if keyword:
        query["keyword"] = keyword
    if category:
        query["category"] = category
    if duration:
        query["duration"] = duration

    return db.find(query)

# ----------------------------------------- #
# challenge page


@app.get("/challenge/{challenge_id}")
async def get_challenge(challenge_id: str):
    return challenges.find_one({"challenge_id": challenge_id})


@app.get("/challenge/{challenge_id}/day/{day}")
async def get_challenge_day(challenge_id: str, day: int):
    return db.find_one({"challenge_id": challenge_id, "day": day})


@app.patch("/challenge/{challenge_id}/join")
def join_challenge(challenge_id: str, user_id: str):
    # add user to challnege joiners list
    return db.update_one({"challenge_id": challenge_id}, {"$push": {"joiners": user_id}})

# ----------------------------------------- #
# create challenge page


@app.post("/create")
def create_challenge():
    challenge: dict = {
        "challenge_id": "123",
        "created_by": "123",
        
    }
    # create a number of days based on challenge duration
    days = [
        {
            "id": i+1,
            "description": "",
            "excercises": []
        }
        for i in range(challenge["duration"])
    ]
    challenge["days"] = days

    return db.insert_one(challenge)


@app.patch("/create/{challenge_id}")
def update_challenge_details(challenge_id: str, challenge: dict):
    # check if duration has been updated
    before_update = db.test.find_one({"challenge_id": challenge_id})
    duration_change = challenge["duration"] - before_update["duration"]
    if duration_change != 0:
        # add or remove modules based on duration change
        if duration_change > 0:
            # add modules
            days = [
                {
                    "id": i+1,
                    "description": "",
                    "excercises": []
                }
                for i in range(before_update["duration"], challenge["duration"])
            ]
            challenge["days"] += days
        else:
            # remove modules
            challenge["days"] = challenge["days"][:duration_change]

    return db.update_one({"challenge_id": challenge_id}, {"$set": challenge})


@app.patch("/create/{challenge_id}/day/{day_id}")
async def save_challenge_day(challenge_id: str, day_id: int, day: dict):
    return db.update_one({"challenge_id": challenge_id, "day.id": day_id}, {"$set": day})


@app.patch("/create/{challenge_id}/day/{day_id}")
def add_excercise_to_day(challenge_id: str, day_id: int, excercise: dict):
    return db.update_one({"challenge_id": challenge_id, "day.id": day_id}, {"$push": {"day.excercises": excercise}})

# ----------------------------------------- #
# dashboard page


@app.get("/dashboard")
async def get_user_challenges(user_id):
    created = db.find({"created_by": user_id})
    joined = db.find({"joiners": user_id})

    return {"created": created, "joined": joined}
