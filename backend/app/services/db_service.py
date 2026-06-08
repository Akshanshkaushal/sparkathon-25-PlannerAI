import logging
import os
from datetime import datetime

from pymongo import ASCENDING, MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)


class DBService:
    def __init__(self):
        try:
            mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
            self.client = MongoClient(mongo_uri)
            self.client.admin.command("ping")
            self.db = self.client.get_database("planner_ai")
            self.parsed_events = self.db.parsed_events
            self.agent_runs = self.db.agent_runs

            indexes = self.parsed_events.index_information()
            if "summary_1" not in indexes:
                self.parsed_events.create_index([("summary", ASCENDING)], unique=True)
            self.agent_runs.create_index([("summary", ASCENDING), ("generated_at", ASCENDING)])

            logger.info("Connected to MongoDB and ensured planner indexes.")
        except ConnectionFailure as exc:
            logger.error("Could not connect to MongoDB: %s", exc)
            raise
        except Exception as exc:
            logger.error("Initialization error: %s", exc)
            raise

    def create_or_update_event_user(self, summary: str, data_to_update: dict):
        if not summary:
            raise ValueError("Summary is required.")

        data_to_update["summary"] = summary
        data_to_update["last_updated"] = datetime.utcnow().isoformat()

        try:
            result = self.parsed_events.update_one(
                {"summary": summary},
                {"$set": data_to_update, "$setOnInsert": {"created_at": datetime.utcnow()}},
                upsert=True,
            )
            if result.upserted_id:
                logger.info("Created new document for summary: %s", summary)
            elif result.modified_count > 0:
                logger.info("Updated existing document for summary: %s", summary)
            else:
                logger.info("No changes made for summary: %s", summary)
            return result
        except Exception:
            logger.exception("Failed to update document for summary: %s", summary)
            raise

    def get_user_by_summary(self, summary: str):
        try:
            return self.parsed_events.find_one({"summary": summary})
        except Exception:
            logger.exception("Could not fetch user by summary: %s", summary)
            raise

    def list_all_summaries(self):
        try:
            cursor = self.parsed_events.find({}, {"summary": 1, "_id": 0})
            return [doc.get("summary") for doc in cursor]
        except Exception:
            logger.exception("Failed to list summaries")
            return []

    def save_agent_run(self, summary: str, result: dict):
        if not summary:
            raise ValueError("Summary is required.")
        return self.agent_runs.insert_one(
            {
                "summary": summary,
                "generated_at": datetime.utcnow().isoformat(),
                "result": result,
            }
        )

    def get_latest_agent_run(self, summary: str):
        return self.agent_runs.find_one(
            {"summary": summary},
            {"_id": 0},
            sort=[("generated_at", -1)],
        )


db_service = DBService()


def get_user_preferences(user_name):
    try:
        user_prefs = db_service.db.user_preferences.find_one({"user_name": user_name})
        if user_prefs:
            return user_prefs.get("preferences", {})

        logger.warning("No preferences found for user: %s", user_name)
        return {}
    except Exception:
        logger.exception("Error retrieving preferences for user: %s", user_name)
        return {}


def add_user_preference(user_name, preferences):
    try:
        result = db_service.db.user_preferences.update_one(
            {"user_name": user_name},
            {"$set": {"preferences": preferences, "updated_at": datetime.utcnow()}},
            upsert=True,
        )
        logger.info("Updated preferences for user: %s", user_name)
        return result
    except Exception:
        logger.exception("Error adding preferences for user: %s", user_name)
        raise
