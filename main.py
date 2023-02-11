import users, challenges, days, exercises
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter


# ---------- configure FASTAPI app ---------- #

app = FastAPI()

app.include_router(users.router)
app.include_router(challenges.router)
app.include_router(days.router)
app.include_router(exercises.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------- root message -------------- #

@app.get("/")
async def success_message():
    return {"message": "Welcome to Thirty Days!"}
