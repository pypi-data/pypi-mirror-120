import datetime
from calendar import monthrange
import optparse
import re
import eel,sys
from calendarcli.dataManager import selectAllTableOnMounth

@eel.expose
def getDayList(date):
    d = str(datetime.date.today()).replace('-0','-')
    try:
        diff = getDifDay(date)
        event = selectAllTableOnMounth(date.year,date.month)
        
    except :
        print(date)
        date = re.split((r'\D+'), date)
        date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
        diff = getDifDay(date)
        event = selectAllTableOnMounth(date.year,date.month)

    print(event)
    data = list()
    if diff['current'][0] != 6:
        for i in range(diff['previous'][1]-diff['current'][0], diff['previous'][1]+1):
            data.append((i,'day day--disabled',''))

    for i in range(1,diff['current'][1]+1):
        data.append([i,'day',f'd{date.year}-{date.month}-{i}'])
        if f"{date.year}-{date.month}-{i}" == str(d):
            print("Get current date...")
            data[-1][1] += " today"

    if len(data)%7 != 0:
        for i in range(1,8-(len(data)%7)):
            data.append((i,'day day--disabled',''))

    return [data,event]

def getDifDay(date:datetime.date):
    cur = monthrange(date.year,date.month)
    try:
        prev = monthrange(date.year, date.month-1)

    except:
        prev = monthrange(date.year-1, 12)
    
    return {
        'current' : cur,
        'previous': prev
    }
