from datetime import datetime
import eel,re
from calendarcli.dataManager import insertData

@eel.expose
def upload(event:str,date:str,detail:str):
    print("\n\n\nuploading...")
    print(event,date,detail)
    date = [int(x) for x in re.split((r'\D+'), date)]
    date = datetime(date[0],date[1],date[2]).date()
    
    insertData(event,date,detail)