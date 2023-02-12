from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.environ.get('MONGODB_URI')

client = AsyncIOMotorClient(MONGODB_URI)

db = client.get_database("ThirtyDays")
challenges_db = db["Challenges"]
exercises_db = db["Exercises"]
users_db = db["Users"]