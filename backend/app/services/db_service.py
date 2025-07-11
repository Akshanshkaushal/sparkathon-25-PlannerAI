import os
import logging
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
from datetime import datetime

logger = logging.getLogger(__name__)

class DBService:
    def __init__(self):
        try:
            mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
            self.client = MongoClient(mongo_uri)
            self.client.admin.command('ping')  # Check connection
            self.db = self.client.get_database("planner_ai")
            self.parsed_events = self.db.parsed_events

            # Ensure unique index on summary (used as unique ID now)
            indexes = self.parsed_events.index_information()
            if 'summary_1' not in indexes:
                self.parsed_events.create_index([("summary", ASCENDING)], unique=True)

            logger.info("✅ Connected to MongoDB and ensured index on summary.")
        except ConnectionFailure as e:
            logger.error(f"❌ Could not connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Initialization error: {e}")
            raise

    def create_or_update_event_user(self, summary: str, data_to_update: dict):
        if not summary:
            raise ValueError("Summary (used as ID) is required.")

        # Always update summary field
        data_to_update["summary"] = summary
        data_to_update["last_updated"] = datetime.utcnow().isoformat()

        try:
            result = self.parsed_events.update_one(
                {"summary": summary},
                {"$set": data_to_update, "$setOnInsert": {"created_at": datetime.utcnow()}},
                upsert=True
            )
            if result.upserted_id:
                logger.info(f"✅ Created new document for summary: {summary}")
            elif result.modified_count > 0:
                logger.info(f"✅ Updated existing document for summary: {summary}")
            else:
                logger.info(f"ℹ️ No changes made for summary: {summary}")
            return result
        except Exception as e:
            logger.error(f"❌ Failed to update document for summary: {summary}, Error: {e}")
            raise

    def get_user_by_summary(self, summary: str):
        try:
            return self.parsed_events.find_one({"summary": summary})
        except Exception as e:
            logger.error(f"❌ Could not fetch user by summary {summary}: {e}")
            raise

    def list_all_summaries(self):
        try:
            cursor = self.parsed_events.find({}, {"summary": 1, "_id": 0})
            return [doc.get("summary") for doc in cursor]
        except Exception as e:
            logger.error("❌ Failed to list summaries")
            return []

# Singleton
db_service = DBService()

# Add the missing functions that are imported in routes.py
def get_user_preferences(user_name):
    """
    Retrieve user preferences from the database.
    
    Args:
        user_name: The name of the user whose preferences to retrieve.
        
    Returns:
        A dictionary of user preferences or empty dict if none found.
    """
    try:
        db = db_service.db
        user_prefs = db.user_preferences.find_one({"user_name": user_name})
        if user_prefs:
            return user_prefs.get("preferences", {})
        else:
            logger.warning(f"No preferences found for user: {user_name}")
            return {}
    except Exception as e:
        logger.error(f"Error retrieving preferences for {user_name}: {e}")
        return {}

def add_user_preference(user_name, preferences):
    """
    Add or update user preferences in the database.
    
    Args:
        user_name: The name of the user to update preferences for.
        preferences: The preferences data to store.
        
    Returns:
        The result of the database operation.
    """
    try:
        db = db_service.db
        result = db.user_preferences.update_one(
            {"user_name": user_name},
            {"$set": {"preferences": preferences, "updated_at": datetime.utcnow()}},
            upsert=True
        )
        logger.info(f"Updated preferences for user {user_name}")
        return result
    except Exception as e:
        logger.error(f"Error adding preferences for {user_name}: {e}")
        raise
