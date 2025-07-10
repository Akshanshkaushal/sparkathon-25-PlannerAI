from apscheduler.schedulers.background import BackgroundScheduler
from credential_store import get_all_users
from calendar_utils import get_events

def scheduled_job():
    print("🕒 Running scheduled event fetch...")
    users = get_all_users()
    for email in users:
        get_events(email)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', hours=24)
    scheduler.start()
    print("📅 Scheduler started")
