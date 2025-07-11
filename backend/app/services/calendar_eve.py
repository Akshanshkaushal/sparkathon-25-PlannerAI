from flask import Flask, redirect, session, url_for, request, jsonify, render_template
from flask_session import Session
from google_auth_oauthlib.flow import Flow
from app.services.credential_store import  store_user_credentials
from app.services.calendar_utils import get_events
from app.services.scheduler import start_scheduler
from dotenv import load_dotenv
from tempfile import gettempdir
import os


# 🔧 Load environment variables
print("\U0001F527 Loading environment variables...")
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "dev"
print("\U0001F511 Secret key set:", app.secret_key[:5] + "...")

# ✅ Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(gettempdir(), 'flask_session')
app.config['SESSION_COOKIE_SECURE'] = False
Session(app)
print(f"\u2705 Flask session initialized using {app.config['SESSION_FILE_DIR']}")

# 🔐 Google OAuth config
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
REDIRECT_URI = 'https://localhost:5000/oauth2callback'
print("🔗 OAuth config - Redirect URI:", REDIRECT_URI)

def credentials_to_dict(creds):
    print("🔐 Converting credentials to dict...")
    return {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

@app.route('/')
def home():
    print("🌐 GET / - Rendering homepage")
    return render_template("index.html")

@app.route('/authorize', methods=['POST'])
def authorize():
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "Email required"}), 400
    session['email'] = email
    print("📨 Received email:", email)

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
    print("🔑 Session state stored:", state)
    print("\u27a1\ufe0f Redirecting to Google OAuth URL:", auth_url)
    return redirect(auth_url)

@app.route('/oauth2callback')
def oauth2callback():
    try:
        print("🔙 Received callback from Google with URL:", request.url)
        state = session.get('state')
        print("🔍 Retrieved session state:", state)
        if not state:
            return '❌ Missing session state. Cannot validate OAuth flow.', 400

        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        email = session.get('email')
        if not email:
            return "Missing email in session", 400

        store_user_credentials(email, credentials_to_dict(credentials))
        get_events(email)
        print(f"✅ OAuth success! Credentials stored and events fetched for {email}")
        return redirect(url_for('home'))

    except Exception as e:
        print(f"❌ OAuth error during callback: {e}")
        return f"OAuth Error: {e}", 400

@app.route('/api/scheduled/<email>')
def show_events(email):
    from pymongo import MongoClient
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["planner_ai"]
    events = list(db.parsed_events.find({"email": email}, {"_id": 0}))
    return jsonify(events)

def create_calendar_app():
    print("🚀 Starting calendar app...")
    
    # Register API blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Start the scheduler
    start_scheduler()
    
    return app