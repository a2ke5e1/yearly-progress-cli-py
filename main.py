from time import sleep
from datetime import datetime

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
    



year = datetime.now().year
month = month_name(datetime.now().month)
day = ordinal(datetime.now().day)




import os
# os.system("cls")


print("Yearly Progress v0.1")
print("--------------------")
try:
    while True:
    
        year_progress = progress('year') * 100
        month_progress = progress('month') * 100
        day_progress = progress('day') * 100

        yi = int(year_progress) // 10
        mi = int(month_progress) // 10
        di = int(day_progress) // 10



        print(f"\nYear: {year}")
        print("[","=" * yi," " * (10 - yi), "]"," {:.8f}%".format(year_progress), sep="")
        print(f"\nMonth: {month}")
        print("[","=" * mi," " * (10 - mi), "]"," {:.8f}%".format(month_progress), sep="")
        print(f"\nDay: {day}")
        print("[","=" * di," " * (10 - di), "]"," {:.8f}%".format(day_progress), sep="")

        print("\033[A" * 10)
        sleep(0.1)

except KeyboardInterrupt:
    print("\n"* 10)
