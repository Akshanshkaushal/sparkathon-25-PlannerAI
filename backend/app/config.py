import os
from threading import Lock

class ConfigSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConfigSingleton, cls).__new__(cls)
                cls._instance.SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-secret-key'
                cls._instance.MONGO_URI = os.environ.get('MONGO_URI')
                cls._instance.AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
                cls._instance.AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
                cls._instance.AZURE_OPENAI_GPT_DEPLOYMENT_NAME = os.environ.get('AZURE_OPENAI_GPT_DEPLOYMENT_NAME')
            return cls._instance
