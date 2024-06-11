from time import sleep
from datetime import datetime
import sys

VERSION = "v0.5"

class FontStyle:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

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

def print_title(title, value):
    print(f"{FontStyle.BOLD}{title}: {FontStyle.END}{value}")

def progress_bar(progress, size=50):
    window_col, _ = get_window_size()

    if window_col < size:
        size = window_col - 30

    if progress > 1:
        progress = 1

    print(f"{FontStyle.BLUE}[{'█' * int(progress * size)}{' ' * int(size - progress * size)}]{FontStyle.END}", f" {(progress*100):.8f}%", sep="")


def get_window_size():
    import os
    col, row = os.get_terminal_size()
    return col, row


year = datetime.now().year
month = month_name(datetime.now().month)
day = ordinal(datetime.now().day)

line_count = 0

def print(*args, **kwargs):
    global line_count
    line_count += 1
    for arg in args:
        line_count += str(arg).count("\n")
    # __builtins__.print(f"{line_count=}")
    __builtins__.print(*args, **kwargs)


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
        __builtins__.print("Create an event: ")
        event["title"] = input("title: ")
        event["description"] = input("description: ")
        event["start_time"] = datetime.strptime(input("Start time (YYYY-MM-DD HH:MM:SS): "), "%Y-%m-%d %H:%M:%S")
        event["end_time"] = datetime.strptime(input("End time (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M:%S")
        events.append(event)
        save_events(events)
    except ValueError:
        __builtins__.print("Invalid date format")
        sys.exit(1)


def main(): 
    global line_count
    keep_looping = True

    show_day = False
    show_month = False
    show_year = False
    show_events = False

    args = sys.argv[1:]
    if args:
        if args[0] == "-h" or  args[0] == "--help":
            __builtins__.print(f"Yearly Progress {FontStyle.BLUE}{VERSION}{FontStyle.END}")
            __builtins__.print("-h --help: Show this help message")
            __builtins__.print("-d --day: Show only the progress of the day")
            __builtins__.print("-m --month: Show only the progress of the month")
            __builtins__.print("-y --year: Show only the progress of the year")
            __builtins__.print("-s : Don't keep updating the progress bar")
            __builtins__.print("-ce --create-event: Create an event")
            __builtins__.print("-l --list: List all events")
            sys.exit(0)

        if "-s" in args:
            keep_looping = False

            if len(args) == 1:
                show_day = True
                show_month = True
                show_year = True

        if "-d" in args or "--day" in args:
            show_day = True
        
        if "-m" in args or "--month" in args:
            show_month = True

        if "-y" in args or "--year" in args:
            show_year = True

        if "-ce" in args or "--create-event" in args:
            create_event()
            sys.exit(0)

        if "-l" in args or "--list" in args:
            show_events = True
    else:
        show_day = True
        show_month = True
        show_year = True
    

    try:
        i = 0
        while keep_looping or i < 1:
            line_count = 0

            print(f"\nYearly Progress {FontStyle.BLUE}{VERSION}{FontStyle.END}")
            print("--------------------")

        
            year_progress = progress('year')
            month_progress = progress('month') 
            day_progress = progress('day') 

    

            if show_year:
                print_title("Year", year)
                progress_bar(year_progress)
                print(f"of {get_total_type_seconds('year')}s")

            if show_month:
                print_title("Month", month)
                progress_bar(month_progress)
                print(f"of {get_total_type_seconds('month')}s")

            if show_day:
                print_title("Day", day)
                progress_bar(day_progress)
                print(f"of {get_total_type_seconds('day')}s")

            if show_events:
                events = load_events()
                for event in events:
                    print_title("\nEvent", event["title"])
                    print_title("Description", event["description"])
                    progress_bar(progress('custom', event["start_time"], event["end_time"]))
                    print(f"from {event['start_time']} to {event['end_time']}")


            print("\033[A" * (line_count + 1)) # plus one for the clear command itself. 
            # get_window_size()
            sleep(0.1)
            i += 1
        
        print("\n"* (line_count))

    except KeyboardInterrupt:
        print("\n"* (line_count))
        sys.exit(0)



if __name__ == "__main__":
    main()