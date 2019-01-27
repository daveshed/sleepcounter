"""
Event objects module
"""
import datetime
import logging
from math import ceil

from sleepcounter.time.bedtime import SleepChecker

LOGGER = logging.getLogger("event")
_SECONDS_PER_DAY = 24 * 3600


class SpecialDay:
    """
    A custom event object that defines a special day. Note that it will be
    a recurring event - it will happen every year on the same day.
    """
    def __init__(self, name, month, day):
        self._name = name
        self._month = month
        self._day = day

    @property
    def name(self):
        """
        Returns the name of the event
        """
        return self._name

    @property
    def month(self):
        """
        Returns the month of the event
        """
        return self._month

    @property
    def day(self):
        """
        Returns the day of the event
        """
        return self._day

    @property
    def date(self):
        """
        Gets the date of the event as a datetime.date object. Will always return
        a date in the future.
        """
        result = None
        this_year = datetime.date(
            year=datetime.datetime.today().year,
            month=self.month,
            day=self.day)
        next_year = datetime.date(
            year=datetime.datetime.today().year + 1,
            month=self.month,
            day=self.day)
        if self._in_future(this_year):
            result = this_year
        elif self.today:
            result = this_year
        else:
            result = next_year
        return result

    @property
    def seconds_remaining(self):
        """Returns the number of seconds to a given event"""
        return self._seconds_until(self.date)

    @staticmethod
    def _seconds_until(date):
        target_time = datetime.datetime.combine(date, SleepChecker.WAKE_UP_TIME)
        delta = target_time - datetime.datetime.today()
        seconds = delta.total_seconds()
        return seconds

    @staticmethod
    def _in_future(date):
        # pylint: disable=protected-access
        return __class__._seconds_until(date) > 0

    @property
    def sleeps_remaining(self):
        """Return the number of sleeps to a until the event"""
        sleeps = ceil(self.seconds_remaining / _SECONDS_PER_DAY)
        LOGGER.info("%s sleeps to event %s", sleeps, self.name)
        return sleeps

    @property
    def today(self):
        """
        Checks whether today is a special day returns the result as a bool
        """
        special = False
        if SleepChecker.is_nighttime():
            LOGGER.info("It's nighttime right now. Wait until morning")
        else:
            today = datetime.datetime.today()
            month_matches = self.month == today.month
            day_matches = self.day == today.day
            special = month_matches and day_matches
            LOGGER.info(
                "The date is %s. It's %s",
                today,
                (self.name if special else "not a special day"))
        return special

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __hash__(self):
        # must define a custom has since we have overriden __eq__
        return id(self)
