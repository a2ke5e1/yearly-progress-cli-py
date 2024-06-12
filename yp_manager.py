from datetime import datetime
from font_style import FontStyle

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix


def month_name(n):
    return ['January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December'][n - 1]

def progress(type, start_time=None, end_time=None):

    start_time = get_start_time(type, start_time)
    end_time = get_end_time(type, end_time)

    total = end_time - start_time
    current = datetime.now() - start_time
    return current / total

def get_start_time(type, start_time=None):
    if type == 'year':
        return datetime(datetime.now().year, 1, 1, 0, 0, 0, 0)
    elif type == 'month':
        return datetime(datetime.now().year, datetime.now().month, 1, 0, 0, 0, 0)
    elif type == 'day':
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0, 0)
    elif type == 'custom' and start_time is not None:
        return start_time


def get_end_time(type, end_time=None):
    if type == 'year':
        return datetime(datetime.now().year, 12, 31, 23, 59, 59, 999999)
    elif type == 'month':
        return datetime(datetime.now().year, datetime.now().month, 30, 23, 59, 59, 999999)
    elif type == 'day':
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59, 999999)
    
    elif type == 'custom' and end_time is not None:
        return end_time

def get_total_type_seconds(type):
    start_time = get_start_time(type)
    end_time = get_end_time(type)
    total_seconds =  (end_time - start_time).total_seconds()

    return int(round(total_seconds, 0))



def get_window_size():
    import os
    col, row = os.get_terminal_size()
    return col, row



def load_events():
    import json
    try:
        events = []
        with open("events.json", "r") as f:
            events = json.load(f)

        for event in events:
            if "start_time" in event:
                event["start_time"] = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M:%S")
            if "end_time" in event:
                event["end_time"] = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M:%S")

        return events
    except FileNotFoundError:
        return []
    
def save_events(events):
    import json
    with open("events.json", "w") as f:
        json.dump(events, f, indent=4, default=str)


def create_event():
    try:
        events = load_events()
        event = {}
        print("Create an event: ")
        event["title"] = input("title: ")
        event["description"] = input("description: ")
        event["start_time"] = datetime.strptime(input("Start time (YYYY-MM-DD HH:MM:SS): "), "%Y-%m-%d %H:%M:%S")
        event["end_time"] = datetime.strptime(input("End time (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M:%S")
        events.append(event)
        save_events(events)
    except ValueError:
        print("Invalid date format")