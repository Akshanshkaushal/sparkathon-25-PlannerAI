from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.environ['MONGO_URI'])
db = client.get_database()
parsed_events_collection = db['parsed_events']

@app.route('/api/scheduled/<email>')
def get_scheduled_events(email):
    events = list(parsed_events_collection.find({'email': email}, {'_id': 0}).sort('timestamp', 1))
    return jsonify(events)
