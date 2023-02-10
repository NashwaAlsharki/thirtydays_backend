from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
import os

# ---------- connect to mongo database ---------- #
load_dotenv()
MONGODB_URI = os.environ.get('MONGODB_URI')
client = AsyncIOMotorClient(MONGODB_URI)
db = client.ThirtyDays
challenges_db = db["Challenges"]
exercises_db = db["Exercises"]
users_db = db["Users"]

# ---------- create FASTAPI app ---------- #
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
