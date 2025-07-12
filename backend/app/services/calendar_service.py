# app/services/calendar_scheduler.py

import logging
import requests
from datetime import date, timedelta
from flask import current_app

# This function should be moved to your db_service.py and implemented
# to query your actual database for events.
def get_upcoming_events(target_date: date):
    """
    Queries the database for events scheduled for the target_date.
    
    Args:
        target_date: The date to check for events.
        
    Returns:
        A list of event objects (e.g., dicts) for the target date.
    
    NOTE: This is a MOCK IMPLEMENTATION for demonstration. You must
    replace this with a real query to your events table in the database.
    """
    logging.info(f"Searching for events on: {target_date}")
    
    # Example mock data that would come from your database
    mock_events_from_db = [
        {"event_id": 1, "event_date": date.today() + timedelta(days=5), "event_type": "Birthday", "person_name": "Alice", "spending_tier": "Mid-Range"},
        {"event_id": 2, "event_date": date.today() + timedelta(days=5), "event_type": "Anniversary", "person_name": "Bob", "spending_tier": "High-End"},
        {"event_id": 3, "event_date": date.today() + timedelta(days=10), "event_type": "Birthday", "person_name": "Charlie", "spending_tier": "Low-Range"},
    ]
    
    upcoming = [event for event in mock_events_from_db if event['event_date'] == target_date]
    return upcoming

def trigger_agent_for_event(event: dict):
    """
    Triggers the planning agent for a single event by making an API call
    to the /trigger-event endpoint.
    """
    # NOTE: Ensure your Flask app's host and port are correct.
    # In production, use environment variables for this URL.
    api_url = "https://127.0.0.1:5000/api/trigger-event"
    headers = {"Content-Type": "application/json"}
    payload = {
        "event_type": event["event_type"],
        "person_name": event["person_name"],
        "spending_tier": event["spending_tier"]
    }
    
    try:
        logging.info(f"SCHEDULER: Triggering agent for event: {event['event_type']} for {event['person_name']}")
        response = requests.post(api_url, json=payload, headers=headers, verify=False)  # verify=False for self-signed cert
        response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
        logging.info(f"SCHEDULER: Successfully triggered agent for event_id {event.get('event_id')}. Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"SCHEDULER: Failed to trigger agent for event_id {event.get('event_id')}. Error: {e}")

def schedule_daily_event_check():
    """
    This is the main job function that APScheduler will execute.
    
    It runs within the application context to access logs and other extensions.
    It calculates the target date (5 days from now), fetches events for that
    date, and triggers the agent for each one.
    """
    with current_app.app_context():
        logging.info("SCHEDULER: Running daily check for upcoming events...")
        
        # Define the target date as 5 days from the current day
        target_date = date.today() + timedelta(days=5)
        
        events_to_trigger = get_upcoming_events(target_date)
        
        if not events_to_trigger:
            logging.info(f"SCHEDULER: No events found for the target date: {target_date}.")
            return

        for event in events_to_trigger:
            trigger_agent_for_event(event)