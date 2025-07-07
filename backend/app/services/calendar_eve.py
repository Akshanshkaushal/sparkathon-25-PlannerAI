from flask import Flask, redirect, session, url_for, request, jsonify
from flask_session import Session
from google_auth_oauthlib.flow import Flow
from calendar_utils import get_events
from credential_store import store_user_credentials, get_user_credentials
from scheduler import start_scheduler
from event_cache import get_cached_events
import os

app = Flask(__name__)

# Fixed dev key for consistent session behavior
app.secret_key = b'super-dev-key'

# Secure session cookies for cross-site Google OAuth redirects
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_HTTPONLY=True
)

# Flask session config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# Google OAuth setup
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
REDIRECT_URI = 'https://localhost:5000/oauth2callback'


@app.route('/')
def index():
    return jsonify({"message": "Send POST to /authorize with 'email' in form-data"})


@app.route('/authorize', methods=['POST'])
def authorize():
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "Email required"}), 400

    session['email'] = email

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return jsonify({"auth_url": auth_url})


@app.route('/oauth2callback')
def oauth2callback():
    if 'state' not in session or 'email' not in session:
        return jsonify({"error": "Session expired. Start again from /authorize"}), 400

    returned_state = request.args.get("state")
    if returned_state != session['state']:
        return jsonify({"error": "CSRF Warning: state mismatch"}), 400

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=session['state'],
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    store_user_credentials(session['email'], {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    })

    return jsonify({"message": f"Credentials stored for {session['email']}"})


@app.route('/api/events/<email>')
def api_events(email):
    credentials = get_user_credentials(email)
    if not credentials:
        return jsonify({'error': 'Not connected'}), 404

    events = get_events(credentials, days_ahead=5)
    return jsonify(events)


@app.route('/api/scheduled/<email>')
def get_scheduled_events(email):
    events = get_cached_events(email)
    return jsonify(events)


# ✅ Expose app for use in run.py
def create_calendar_app():
    start_scheduler()
    return app
