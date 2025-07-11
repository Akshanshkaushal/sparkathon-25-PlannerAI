import os
import datetime
from pymongo import MongoClient
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.services.credential_store import get_user_credentials

def get_events(email):
    creds_dict = get_user_credentials(email)
    if not creds_dict:
        print(f"⚠️ No credentials found for {email}")
        return

    credentials = Credentials(
        token=creds_dict['token'],
        refresh_token=creds_dict.get('refresh_token'),
        token_uri=creds_dict['token_uri'],
        client_id=creds_dict['client_id'],
        client_secret=creds_dict['client_secret'],
        scopes=creds_dict['scopes']
    )

    service = build('calendar', 'v3', credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=5)).isoformat() + 'Z'

    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=time_max,
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
    except Exception as e:
        print(f"❌ Error fetching events for {email}: {e}")
        return

    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["planner_ai"]

    db.parsed_events.delete_many({"email": email})

    for event in events:
        event['email'] = email

    if events:
        db.parsed_events.insert_many(events)
        print(f"✅ Inserted {len(events)} events for {email}")
    else:
        print(f"ℹ️ No upcoming events found for {email}")
