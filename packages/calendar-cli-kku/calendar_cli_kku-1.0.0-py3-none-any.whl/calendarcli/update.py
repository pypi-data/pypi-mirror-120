from calendarcli.check import isDate
from colorama import Style, Back, Fore
import sys, datetime

id = str()
oldEvent = str()
newEvent = str()
newDate = str()
confirm = False


def data(a, opt):
    global oldEvent
    global newDate
    global newEvent
    global id
    global confirm
    try:
        id = int(a)
    except :
        oldEvent = a
    if not opt:
        print("Pleas enter data to update. or --help")
        sys.exit()
    for i, j in opt:
        if i in ("--date", '-d'):
            if isDate(j):
                newDate = j
            else:
                print(Fore.YELLOW + f"Date format {a} not match")
                print(
                    f"Please enter in yyy-mm-dd such as {Back.MAGENTA} {datetime.datetime.today().date()} " + Style.RESET_ALL)
                sys.exit()

        elif i in ("--event", '-e'):
            newEvent = j
        
        elif i == '--confirm':
            confirm = True
        
        else: print(i,"is not option!")

    # print(id, oldEvent, "-->", newDate, newEvent)

    # updating...
    from calendarcli.dataManager import update
    from calendarcli.dataManager import searchEvent,searchID
    if oldEvent:
        data = searchEvent(oldEvent)
        if len(data)==1:
            update(oldEvent,newDate,newEvent)
            print(Fore.GREEN+"successful"+Fore.RESET)
            
        elif len(data)<1:
            print("No event match with",oldEvent)
            data = searchEvent(f"%{oldEvent}%")
            for i,d in enumerate(data):
                if i == 0:print("\nSomething similar",oldEvent)
                print(f"  ├─{d[1]} {d[2]} (ID = {d[0]}])'")
            print()

        else:
            print("Seem like It has more than one event.")
            for i in data:
                print(f"  ├─{i[1]} {i[2]} (ID = {i[0]})'")
            print()
            if confirm:
                update(oldEvent,newDate,newEvent)
                print(Fore.GREEN+"successful"+Fore.RESET)
            elif input("Do you want to Update all? (N:y) ").upper() =="Y":
                update(oldEvent,newDate,newEvent)
                print(Fore.GREEN+"successful"+Fore.RESET)
    else:
        event = searchID(id)
        if len(event)>0:
            update(id,newDate,newEvent)
            print(Fore.GREEN+"successful"+Fore.RESET)
        
        else:
            print("ID =",id, "dose not exit.")
