# event_cache.py

event_cache = {}

def update_user_events(email, events):
    event_cache[email] = events

def get_cached_events(email):
    return event_cache.get(email, [])

def get_all_cached():
    return event_cache
