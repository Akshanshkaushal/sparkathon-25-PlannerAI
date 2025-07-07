from app.services.calendar_eve import create_calendar_app

app = create_calendar_app()

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)
