## Thirty Days - Backend
Thirty Days is an application where users can discover and craft challenges. Each challenge comprises daily modules, which can include a text description, illustrated exercises, or a combination of both.

## Prerequisites
An active MongoDB account.
Python 3.8 or newer installed.

## Setup & Installation
1. Clone the Repository:
```
git clone <repository-link> thirtydays_backend
cd thirty-days-backend
```

2. Set Up a Virtual Environment (Optional, but recommended):
```
python3.8 -m venv venv
source venv/bin/activate
```

4. Install Dependencies:
```
pip install -r requirements.txt
```
5. Environment Variables:
You'll need to set up environment variables for connecting to MongoDB. It's a good practice to maintain a .env file for this purpose (but ensure .env is added to your .gitignore to keep secrets safe). 
6. Running the Application:
With fastapi installed, you can run:
```
uvicorn main:app --reload
```
Replace main with your entry filename if it's different.
