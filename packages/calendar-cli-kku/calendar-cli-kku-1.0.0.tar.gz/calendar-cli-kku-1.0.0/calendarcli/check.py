# Contain boolean functions


import re

def isDate(a): # Check if string formath YYYY-MM-DD
    return len(a)==10 and bool(re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]",a))

