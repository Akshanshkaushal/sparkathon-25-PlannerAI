import os
from flask import Flask
from flask_pymongo import PyMongo
from pymongo import ASCENDING
from app.config import Config

app = Flask(__name__)
app.config["MONGO_URI"] = Config.MONGO_URI

# Initialize PyMongo
db = PyMongo(app)

# Ensure collection with unique index on email (and optionally user_name)
def setup_users_collection():
    users_collection = db.db.users
    # Make sure there is a unique index on email
    users_collection.create_index([("email", ASCENDING)], unique=True)
    # Optional: also unique on user_name
    users_collection.create_index([("user_name", ASCENDING)], unique=True)

# Run once on import
setup_users_collection()

# CRUD Functions
def create_or_update_user(user_name, email, preferences=None, spending_tier=None):
    """
    Creates a new user or updates existing user by email.
    """
    update_fields = {
        "user_name": user_name,
        "email": email
    }
    if preferences is not None:
        update_fields["preferences"] = preferences
    if spending_tier is not None:
        update_fields["spending_tier"] = spending_tier

    db.db.users.update_one(
        {"email": email},
        {"$set": update_fields},
        upsert=True
    )

def get_user_preferences(email):
    user = db.db.users.find_one({"email": email})
    return user.get("preferences", []) if user else []

# Add this function to match the import in routes.py
def get_user_preferences_by_email(email):
    """Alias for get_user_preferences for backward compatibility"""
    return get_user_preferences(email)

def update_user_preferences(email, preferences):
    db.db.users.update_one(
        {"email": email},
        {"$set": {"preferences": preferences}},
        upsert=True
    )

def get_user_spending_tier(email):
    user = db.db.users.find_one({"email": email})
    return user.get("spending_tier") if user else None

# Add this function to match the import in routes.py
def get_user_spending_tier_by_email(email):
    """Alias for get_user_spending_tier for backward compatibility"""
    return get_user_spending_tier(email)

def update_user_spending_tier(email, spending_tier):
    db.db.users.update_one(
        {"email": email},
        {"$set": {"spending_tier": spending_tier}},
        upsert=True
    )
