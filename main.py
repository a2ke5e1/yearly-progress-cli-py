from time import sleep
from datetime import datetime
import sys

VERSION = "v0.4"

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

def progress(type):

    start_time = get_start_time(type)
    end_time = get_end_time(type)

    total = end_time - start_time
    current = datetime.now() - start_time
    return current / total

def get_start_time(type):
    if type == 'year':
        return datetime(datetime.now().year, 1, 1, 0, 0, 0, 0)
    elif type == 'month':
        return datetime(datetime.now().year, datetime.now().month, 1, 0, 0, 0, 0)
    elif type == 'day':
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0, 0)


def get_end_time(type):
    if type == 'year':
        return datetime(datetime.now().year, 12, 31, 23, 59, 59, 999999)
    elif type == 'month':
        return datetime(datetime.now().year, datetime.now().month, 30, 23, 59, 59, 999999)
    elif type == 'day':
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59, 999999)

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


def main(): 
    global line_count
    keep_looping = True

    show_day = False
    show_month = False
    show_year = False

    args = sys.argv[1:]
    if args:
        if args[0] == "-h" or  args[0] == "--help":
            __builtins__.print(f"Yearly Progress {FontStyle.BLUE}{VERSION}{FontStyle.END}")
            __builtins__.print("-h --help: Show this help message")
            __builtins__.print("-d --day: Show only the progress of the day")
            __builtins__.print("-m --month: Show only the progress of the month")
            __builtins__.print("-y --year: Show only the progress of the year")
            __builtins__.print("-s : Don't keep updating the progress bar")
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