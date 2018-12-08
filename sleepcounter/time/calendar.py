import datetime
import logging
from math import ceil

logger = logging.getLogger("calendar")

_WAKE_UP_TIME = datetime.time(
    hour=6,
    minute=30,
    second=0)
_BEDTIME = datetime.time(
    hour=19,
    minute=0,
    second=0)
_SECONDS_PER_DAY = 24 * 3600

class Calendar:
    """
    Interface to the date library that allows you to lookup the next event and 
    find out what is happening today.
    """
    def __init__(self, date_library):
        logger.info("Instantiated with date_library {}".format(date_library))
        self.date_library = date_library

    def seconds_to_event(self, ev):
        target_date = self.date_library.get_date(ev)
        target_time = datetime.datetime.combine(target_date,  _WAKE_UP_TIME)
        delta = target_time - datetime.datetime.today()
        seconds = delta.total_seconds()
        return seconds

    def sleeps_to_event(self, ev):
        sleeps = ceil(self.seconds_to_event(ev) / _SECONDS_PER_DAY)
        logger.info("{} sleeps to event {}".format(sleeps, ev))
        return sleeps

    @property
    def next_event(self):
        # filter out events in the past
        deltas = \
            {ev: self.seconds_to_event(ev) for ev in self.date_library.events 
                if self.seconds_to_event(ev) > 0}
        # get the event with the smallest positive delta
        next_event = min(deltas, key=deltas.get)
        logger.info("Next event is {}".format(next_event))
        return next_event

    @property
    def sleeps_to_next_event(self):
        return self.sleeps_to_event(self.next_event)
    
    @property
    def special_day_today(self):
        special = self.todays_event is not None
        logger.info("Today is special {}".format(special))
        return special

    @property
    def todays_event(self):
        if self.is_nighttime:
            result = None
            logger.info("It's nighttime. Wait till morning.")
        else:
            todays_date = datetime.datetime.today().date()
            result = self.date_library.get_event(todays_date)
            logger.info("Today is %s. The event is %s", todays_date, result)
        return result

    @property
    def seconds_to_next_event(self):
        seconds = self.seconds_to_event(self.next_event)
        logger.info("{} seconds to next event".format(seconds))
        return seconds

    @property
    def is_nighttime(self):
        now = datetime.datetime.now().time()
        return now > _BEDTIME or now < _WAKE_UP_TIME