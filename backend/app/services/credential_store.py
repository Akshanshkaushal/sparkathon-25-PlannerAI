# credential_store.py

import json
import os

CREDENTIALS_FILE = 'user_credentials.json'


def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_credentials(credentials_dict):
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials_dict, f)


def get_user_credentials(email):
    all_credentials = load_credentials()
    return all_credentials.get(email)


def store_user_credentials(email, credentials):
    all_credentials = load_credentials()
    all_credentials[email] = credentials
    save_credentials(all_credentials)
