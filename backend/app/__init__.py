 
from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .api.routes import api_bp
from .services.db_service import db
from .services.calendar_service import schedule_daily_event_check # <-- Import the job function
from flask_apscheduler import APScheduler

# Initialize scheduler
scheduler = APScheduler()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Initialize the scheduler
    scheduler.init_app(app)

    # Add the job to the scheduler within the app context.
    # This job will run the 'schedule_daily_event_check' function every 24 hours.
    # The 'id' is crucial to prevent creating duplicate jobs when the app reloads in debug mode.
    if not scheduler.get_job('daily_event_check_job'):
        scheduler.add_job(
            id='daily_event_check_job', 
            func=schedule_daily_event_check, 
            trigger='interval', 
            hours=24 # The job will run once every 24 hours.
        )
    
    # Start the scheduler
    scheduler.start()

    app.register_blueprint(api_bp, url_prefix='/api')
#
    return app