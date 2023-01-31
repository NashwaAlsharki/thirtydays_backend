import json
from dotenv import load_dotenv
from fastapi import FastAPI
import pymongo
import os

app = FastAPI()

load_dotenv()
DATABASE_URI = os.environ.get('DATABASE_URI')
client = pymongo.MongoClient(DATABASE_URI)
db = client['ThirtyDays']['Test']


@app.post("/test")
def create_test():
    test_item = {
        "details": "test 15",
        "date": "2021-01-15",
        "time": "12:00:00",
        "status": "pending"
    }
    db.insert_one(test_item)
    return {"message": "Test created successfully!"}


@app.get("/test")
def get_test():
    data = db.find()
    return data[0]


f = open('exercises.json')
data = json.load(f)
base_url = 'https://raw.githubusercontent.com/everkinetic/data/main/src/images-web/'


@app.post("/excer")
def add_excer():
    for item in data:
        try:
            names = item['img']
            item['img_link'] = []
            for img in names:
                name = img.split('web/')[1]
                item['img_link'].append(base_url+name)
        except:
            pass

        db.insert_one(item)

    return {"message": "Exercises added successfully!"}
