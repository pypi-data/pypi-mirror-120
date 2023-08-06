import sys
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
    "confirm",
    "start"
]


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], unixOptions, gunOptions)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    try:
        o, a = opts.pop(0)
    except IndexError:
        o = "calendar"

    if o in ("--help", "-h"):
        import calendarcli.help

    elif o in ("--add", "-a"):
        import calendarcli.add as add
        add.data(opts)

    elif o in ("--update", "-u"):
        import calendarcli.update as update
        update.data(a, opts)

    elif o in ("--delete", "-d"):
        from calendarcli.delete import find
        find(a,opts)

    elif o in ("--list", "-l"):
        import calendarcli.list as list
        list.data(a, opts)

    elif o == "calendar":
        import calendarcli.icalendar as icalendar
        icalendar.printCalendar()

    elif o == "--start":
        from calendarcli.calendargui.app import start
        start()

    else:
        import calendarcli.help


if __name__ == '__main__':
    main()
