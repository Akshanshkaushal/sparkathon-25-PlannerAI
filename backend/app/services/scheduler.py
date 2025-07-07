# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from calendar_utils import get_events
from credential_store import load_credentials
from event_cache import update_user_events
from datetime import datetime

def scheduled_job():
    print(f"[{datetime.now()}] Running daily calendar fetch...")
    all_credentials = load_credentials()

    for email, creds in all_credentials.items():
        try:
            events = get_events(creds, days_ahead=5)
            update_user_events(email, events)
            print(f"✅ Cached events for {email}")
        except Exception as e:
            print(f"❌ Failed to fetch events for {email}: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'cron', hour=4, minute=0)  # 4:00 AM every day
    scheduler.start()
    print("📅 Scheduler started")
