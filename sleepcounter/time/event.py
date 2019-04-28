"""
Event objects module
"""
from abc import ABC, abstractmethod
import datetime
import logging
from math import ceil

from sleepcounter.time.bedtime import SleepChecker

LOGGER = logging.getLogger("event")
_SECONDS_PER_DAY = 24 * 3600


class EventBase(ABC):
    """
    A custom event object that defines a special day.

    keyword arguments:
    name -- a string that defines a name for the event for debugging and display
    month -- a numeric representation of the month 1->12
    day -- the day the event occurs
    sleeps -- the number of sleeps to count in the lead-up to the event.
    """
    def __init__(
            self,
            name: str,
            month: int,
            day: int,
            sleeps=None,
        ):
        self._name = name
        self._month = month
        self._day = day
        self._sleeps = sleeps

    @property
    def name(self):
        """
        Returns the name of the event
        """
        return self._name

    @property
    def month(self):
        """Returns the month of the event"""
        return self._month

    @property
    def day(self):
        """Returns the day of the event"""
        return self._day

    @property
    @abstractmethod
    def year(self):
        """Returns the year that the event happens"""

    @property
    @abstractmethod
    def date(self):
        """Returns the date of the event as a datetime object"""

    @property
    def active(self):
        """
        Status of the event. Returns False if the event has expired or is not
        yet due to be displayed, True otherwise.
        """
        result = False
        event_past = self.sleeps_remaining < 0
        if self._sleeps:
            counted_sleeps = self.sleeps_remaining > self._sleeps
            result = not (event_past or counted_sleeps)
        else:
            result = not event_past
        return result

    @property
    def seconds_remaining(self):
        """Returns the number of seconds to a given event"""
        return self._seconds_until(self.date)

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
            special = self.month == today.month and self.day == today.day
            LOGGER.info(
                "The date is %s. It's %s",
                today,
                (self.name if special else "not a special day"))
        return special

    @staticmethod
    def _seconds_until(date):
        target_time = datetime.datetime.combine(date, SleepChecker.WAKE_UP_TIME)
        delta = target_time - datetime.datetime.today()
        seconds = delta.total_seconds()
        return seconds

    def _in_future(self, date):
        return self._seconds_until(date) > 0

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __hash__(self):
        # must define a custom has since we have overriden __eq__
        return id(self)


class Anniversary(EventBase):
    """
    A custom event object that defines a special day that happens the same date
    every year.

    keyword arguments:
    name -- a string that defines a name for the event for debugging and display
    month -- a numeric representation of the month 1->12
    day -- the day the event occurs
    sleeps -- the number of sleeps to count in the lead-up to the event.
    """
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
    def year(self):
        """the year of the event"""
        return self.date.year


class SpecialDay(EventBase):
    """
    A custom event object that defines a special day that only happens once.

    keyword arguments:
    name -- a string that defines a name for the event for debugging and display
    year -- the year of the event
    month -- a numeric representation of the month 1->12
    day -- the day the event occurs
    sleeps -- the number of sleeps to count in the lead-up to the event.
    """
    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name: str,
            year: int,
            month: int,
            day: int,
            sleeps=None,
        ):
        self._year = year
        super().__init__(name, month, day, sleeps)

    @property
    def year(self):
        """the year of the event"""
        return self._year

    @property
    def date(self):
        """
        Gets the date of the event as a datetime.date object. Will always return
        a date in the future.
        """
        return datetime.date(
            year=self.year,
            month=self.month,
            day=self.day)
