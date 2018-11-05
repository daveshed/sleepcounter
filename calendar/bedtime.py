import datetime

WAKEUP = datetime.time(hour=6, minute=30)
BEDTIME = datetime.time(hour=19, minute=0)

def _now():
    return datetime.datetime.now().time()

bedtime = now() > BEDTIME     
wakeytime = not bedtime