import datetime, sys
from colorama import Style, Back, Fore
from calendarcli.check import isDate
from calendarcli.dataManager import insertData

date = datetime.datetime.today().date()
event = str()


def data(opt=[]):  # Receiv option *event and date than check format befor add it into database
    global event
    global date

    for o, a in opt:
        if o in ("--event", "-e"):
            event = a
        elif o in ("--date", "-d"):
            if isDate(a):
                date = a
            else:
                print(Fore.YELLOW + f"Date format {a} not match")
                print(f"Please enter in yyy-mm-dd such as {Back.MAGENTA} {date} " + Style.RESET_ALL)
                sys.exit()
        else:
            print(f"{o} is not option")
            sys.exit()
    try:
        if event:
            insertData(event, date, )
            print(f"{Fore.GREEN}{event} on {date} has added to calendar!!{Fore.RESET}")
        else:
            print(Fore.YELLOW + '--add require option --event=<enter your event>' + Fore.RESET)
    except Exception as e:
        print(f"Erroe -> {e}")
