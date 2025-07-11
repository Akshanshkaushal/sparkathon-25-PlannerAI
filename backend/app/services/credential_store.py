from pymongo import MongoClient
import os

def get_db():
    from dotenv import load_dotenv
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["planner_ai"]

def store_user_credentials(email, creds_dict):
    db = get_db()
    db.user_credentials.update_one(
        {"email": email},
        {"$set": {"credentials": creds_dict}},
        upsert=True
    )

def get_user_credentials(email):
    db = get_db()
    record = db.user_credentials.find_one({"email": email})
    return record["credentials"] if record else None

def get_all_users():
    db = get_db()
    return [doc["email"] for doc in db.user_credentials.find()]
