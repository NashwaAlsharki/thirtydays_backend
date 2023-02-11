from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client["ThirtyDays"]
challenges_db = db["Challenges"]
exercises_db = db["Exercises"]
users_db = db["Users"]