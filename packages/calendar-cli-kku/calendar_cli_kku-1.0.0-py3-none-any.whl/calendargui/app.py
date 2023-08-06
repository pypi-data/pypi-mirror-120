import eel
import sys
from calendargui.createCalendar import getDayList as getday
from calendarcli.path import fullPath

eel.init(fullPath('calendargui/web'))

def start():
    print("start GUI...",'\n',str(fullPath('calendargui/web')))
    print("Prase CLRL + C to stop.")
    eel.start('index.html',disable_cache=True)


@eel.expose
def printtext(s:str):
    print(s)
# @eel.expose
# def getDayList(date):
#     return getday(date)