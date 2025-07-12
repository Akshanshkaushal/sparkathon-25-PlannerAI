# run.py (in root of backend/)
from app.services.calendar_eve import create_calendar_app

app = create_calendar_app()

if __name__ == '__main__':
    app.run(
        host='localhost',  # 👈 Force it to run on localhost (127.0.0.1)
        # ssl_context=('cert.pem', 'key.pem'),  # Commented out for development
        debug=True,
        use_reloader=False
    )
