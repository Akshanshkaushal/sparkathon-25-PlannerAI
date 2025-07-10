# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "a-secret-key")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/planner_ai")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_GPT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT_NAME")
