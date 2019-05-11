"""
Module defining the LedMatrixWidget that represents sleep information using
an LED display.
"""
# pylint: disable=invalid-name
import logging

from sleepcounter.widget.base import BaseWidget
from sleepcounter.display.display import LedMatrix
from sleepcounter.time.calendar import Calendar

LOGGER = logging.getLogger("display widget")


class LedMatrixWidget(BaseWidget):
    """
    Represents the date using an led matrix.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, display: LedMatrix, calendar: Calendar, label=None):
        self._display = display
        super().__init__(calendar, label)

    def update(self):
        """Updates the display using data from the current calendar instance"""
        self._display.clear()
        if self._calendar.special_day_today:
            self._handle_special_day()
        else:
            self._handle_regular_day()

    def _handle_special_day(self):
        msg = "It's {}!".format(self._calendar.todays_event.name)
        LOGGER.info(
            "Updating with calendar %s. Setting message to %s",
            self._calendar, msg)
        self._display.show_message(msg)

    def _handle_regular_day(self):
        for event in self._calendar.events:
            sleeps = self._calendar.sleeps_to_event(event)
            unit = 'sleeps' if sleeps > 1 else 'sleep'
            msg = "{} in {} {}".format(
                event.name, sleeps, unit)
            LOGGER.info(
                "Updating with calendar %s. Setting message to %s",
                self._calendar, msg)
            self._display.clear()
            self._display.show_message(msg)
