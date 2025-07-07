# calendar_utils.py

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta

def get_events(credentials_dict, days_ahead=5):
    creds = Credentials(**credentials_dict)
    service = build('calendar', 'v3', credentials=creds)

    # Target date is X days ahead from today (UTC)
    target_date = datetime.utcnow() + timedelta(days=days_ahead)

    # Define start and end of that day in ISO format
    time_min = target_date.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
    time_max = target_date.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

    result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return result.get('items', [])
