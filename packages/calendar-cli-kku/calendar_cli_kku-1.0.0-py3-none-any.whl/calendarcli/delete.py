import sys
from colorama import Style,Back, Fore

confirm = False

def find(event,opts):
    global confirm
    for i,j in opts:
        if i == "--confirm":confirm = True
        else: print(f"{i} is not option")

    try:
        id = int(event)
        deleteByID(id)

    except:
        deleteByEvent(event)

def deleteByEvent(event):
    global confirm
    from calendarcli.dataManager import searchEvent
    from calendarcli.dataManager import deleteByEvent as delete
    data = searchEvent(event)
    if len(data)==1:
        print("Found event :",data[0][1],data[0][2],f'(ID = {data[0][0]})')

    elif len(data)<1:
        print("No event match with",event)
        data = searchEvent(f"%{event}%")
        for i,d in enumerate(data):
            if i == 0:print("\nsomething similar",event)
            print(f"  ├─{d[1]} {d[2]} (ID = {d[0]}])'")
        print()

    else:
        print("Seem like It has more than one event.")
        for i in data:
            print(f"  ├─{i[1]} {i[2]} (ID = {i[0]}])'")
        print()
        if confirm:
            delete(event)
            print(Fore.GREEN+"successful"+Fore.RESET)
        elif input("Do you want to delete all? (N:y) ").upper() =="Y":
            delete(event)
            print(Fore.GREEN+"successful"+Fore.RESET)

def deleteByID(id):
    global confirm
    from calendarcli.dataManager import searchID
    from calendarcli.dataManager import deleteByID as delete
    event = searchID(id)
    if len(event)>0:
        print("Found event :",event[0][1],event[0][2],f'(ID = {event[0][0]})')
        if not confirm:x=input("Do you want to delete? (N:y)  ")
        else: x = 'y'

        if (confirm or x.upper() == 'Y'):
            delete(id)
            print(Fore.GREEN+"successful"+Fore.RESET)
    
    else:
        print("ID =",id, "dose not exit.")
    