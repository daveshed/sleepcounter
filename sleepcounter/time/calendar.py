"""Module docstring placeholder"""
import datetime
import logging
from math import ceil

LOGGER = logging.getLogger("calendar")

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
        LOGGER.info("Instantiated with date_library %s", date_library)
        self.date_library = date_library

    def seconds_to_event(self, event):
        """Returns the number of seconds to a given event"""
        target_date = self.date_library.get_date(event)
        target_time = datetime.datetime.combine(target_date, _WAKE_UP_TIME)
        delta = target_time - datetime.datetime.today()
        seconds = delta.total_seconds()
        return seconds

    def sleeps_to_event(self, event):
        """Return the number of sleeps to a given event"""
        sleeps = ceil(self.seconds_to_event(event) / _SECONDS_PER_DAY)
        LOGGER.info("%s sleeps to event %s", sleeps, event)
        return sleeps

    @property
    def next_event(self):
        """Get the next event to happen"""
        # filter out events in the past
        deltas = \
            {
                ev: self.seconds_to_event(ev) for ev in self.date_library.events
                if self.seconds_to_event(ev) > 0
            }
        # get the event with the smallest positive delta
        next_event = min(deltas, key=deltas.get)
        LOGGER.info("Next event is %s", next_event)
        return next_event

    @property
    def sleeps_to_next_event(self):
        """Return the number of sleeps to the next event"""
        return self.sleeps_to_event(self.next_event)

    @property
    def special_day_today(self):
        """Checks whether today is a special day registered in the calendar and
        returns the result as a bool"""
        special = self.todays_event is not None
        LOGGER.info("Today is special? %s", special)
        return special

    @property
    def todays_event(self):
        """Returns todays event or None if it's not a special day"""
        if self.is_nighttime:
            result = None
            LOGGER.info("It's nighttime. Wait till morning.")
        else:
            todays_date = datetime.datetime.today().date()
            result = self.date_library.get_event(todays_date)
            LOGGER.info("Today is %s. The event is %s", todays_date, result)
        return result

    @property
    def seconds_to_next_event(self):
        """Returns the time to the next event in seconds"""
        seconds = self.seconds_to_event(self.next_event)
        LOGGER.info("%s seconds to next event", seconds)
        return seconds

    @property
    def is_nighttime(self):
        """Checks whether it's nighttime and returns the result as a bool"""
        now = datetime.datetime.now().time()
        return now > _BEDTIME or now < _WAKE_UP_TIME
