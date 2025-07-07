# anywhere in your Flask backend (another service or route)
import requests

def fetch_calendar_events(email):
    try:
        response = requests.get(f'https://localhost:5000/api/events/{email}', verify=False)  # verify=False for self-signed cert
        if response.status_code == 200:
            events = response.json()
            return events
        else:
            print("Error:", response.status_code, response.text)
            return []
    except Exception as e:
        print("Exception fetching calendar events:", str(e))
        return []
