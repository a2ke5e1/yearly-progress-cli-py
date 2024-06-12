from datetime import datetime
from time import sleep
import sys
from font_style import FontStyle
from yp_manager import month_name, ordinal, progress, get_total_type_seconds, create_event, load_events, get_window_size


VERSION = "v0.6"



def print(*args, **kwargs):
    global line_count
    line_count += 1
    for arg in args:
        line_count += str(arg).count("\n")
    # __builtins__.print(f"{line_count=}")
    __builtins__.print(*args, **kwargs)


def print_title(title, value):
    print(f"{FontStyle.BOLD}{title}: {FontStyle.END}{value}")

def progress_bar(progress, size=50):
    window_col, _ = get_window_size()

    if window_col < size:
        size = window_col - 30

    if progress > 1:
        progress = 1

    print(f"{FontStyle.BLUE}[{'█' * int(progress * size)}{' ' * int(size - progress * size)}]{FontStyle.END}", f" {(progress*100):.8f}%", sep="")


year = datetime.now().year
month = month_name(datetime.now().month)
day = ordinal(datetime.now().day)

line_count = 0



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