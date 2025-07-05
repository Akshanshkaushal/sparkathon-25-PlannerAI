import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-secret-key'
    MONGO_URI = os.environ.get('MONGO_URI')
    AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_GPT_DEPLOYMENT_NAME = os.environ.get('AZURE_OPENAI_GPT_DEPLOYMENT_NAME')