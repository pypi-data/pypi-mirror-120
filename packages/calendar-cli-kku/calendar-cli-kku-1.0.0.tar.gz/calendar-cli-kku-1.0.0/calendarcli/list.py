import sys
from colorama import Style,Back, Fore
from calendarcli.dataManager import selectTableOnMounth
from datetime import datetime

# print("list")

def data(a,o):
    if not not a:
        try :
            a = int(a)
            printXmonth(a)

        except Exception as e :
            if not (a in ("smsm")):
                print(Fore.YELLOW + f"-l{a} is not options!!" + Fore.RESET)
                sys.exit()

            else:
                if "m" in a : editMode()
                else : printStd()

    else:
        # print("--list",o)
        if(('-m', '') in o or ('--modify', '')in o ):
            editMode()
            sys.exit()

        else:
            for i,j in o:
                if i == "-n":
                    try : printXmonth(int(j))
                    except Exception as e:
                        print(Fore.YELLOW + f"{j} is not a number. Please enter only number." + Fore.RESET)

                elif i in ("--search","-s") :
                    search(j)

                else : print(Fore.YELLOW + f"{i} {j} is not option" + Fore.RESET)
                sys.exit()
                
            printStd()


d = datetime.today()

def search(event):
    from calendarcli.dataManager import searchEvent
    data = searchEvent(f"%{event}%")
    print("Search",event,"found",len(data))
    for i in data:
        print(f"  ├─{i}")
    print()

def printXmonth(x):
    fd = d
    for j in range(x):
        data = selectTableOnMounth(curDate=fd.date())
        for index,i in enumerate(data):
            if index == 0 :
                print("\n",f"{Fore.LIGHTCYAN_EX}{fd.strftime('%Y %B')}{Fore.RESET}" )
            print(f"  ├─{i[2]} : {i[1]} (id:{i[0]})")
        try    : fd = datetime(int(fd.year), int(fd.month)+1, 1)
        except : fd = datetime(int(fd.year)+1, 1,1)
    print()


def printStd():
    print("\n",d)
    data = selectTableOnMounth()
    for i in data:
        print(f"  ├─{i[2]} : {i[1]} (id:{i[0]})")
    print()


def editMode():
    from pprint import pprint
    import inquirer

    l = list()
    id = list()
    for index,i in enumerate(selectTableOnMounth()):
        l.append(f"{index+1:^3d} {i[2]} {i[1]}")
        id.append(i[0])
    # print(l)

    questions = [
        inquirer.List('edit',
                        message="What event do you want to modify?",
                        choices=l,
                        carousel=True
                    ),
        
        inquirer.List('mode',
                        message="What do you want to do?",
                        choices=['Delete','Update'],
                        carousel=True
                    ),
    ]
    answers = inquirer.prompt(questions)
    answers['edit'] = id[int(answers['edit'].split()[0])-1]
    del id

    if answers['mode'] == 'Delete':
        input("Press Enter to continue...")
        from calendarcli.dataManager import deleteByID
        deleteByID(answers['edit'])
        print(Fore.GREEN+"successful"+Fore.RESET,'\n')

    else:
        import getopt
        unixOptions = "hau:d:l:me:n:s:"
        gunOptions = [
            "help",
            "add",
            "date=",
            "event=",
            "update=",
            "delete=",
            "list",
            "modify",
            "search=",
            "confirm"
        ]
        arg = input("Enter command\n >> ").split()
        try:
            opts, args = getopt.getopt(arg, unixOptions, gunOptions)
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)
        from calendarcli.update import data as updateEX
        updateEX(answers['edit'],opts)
    