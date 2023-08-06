from datetime import datetime
import eel,re
from calendarcli.dataManager import update

@eel.expose
def updateEvent(id:str,event:str,date:str,detail:str):
    print("\n\nUpdatting...")
    # date = [int(x) for x in re.split((r'\D+'), date)]
    # date = datetime(date[0],date[1],date[2]).date()
    
    print(id,event,date,detail)
    update(id,'',event,str(detail))