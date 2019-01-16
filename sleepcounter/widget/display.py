"""
Module defining the LedMatrixWidget that represents sleep information using
an LED display.
"""
# pylint: disable=invalid-name
import logging

from sleepcounter.widget.base import BaseWidget
from sleepcounter.display.display import LedMatrix

LOGGER = logging.getLogger("display widget")


class LedMatrixWidget(BaseWidget):
    """
    Represents the date using an led matrix.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, display: LedMatrix):
        LOGGER.info("Intantiating")
        self.display = display

    def update(self, calendar):
        """Updates the display using data from the current calendar instance"""
        if calendar.special_day_today:
            self._handle_special_day(calendar)
        else:
            self._handle_regular_day(calendar)

    def _handle_special_day(self, calendar):
        msg = "It's {}!".format(calendar.todays_event)
        LOGGER.info(
            "Updating with calendar %s. Setting message to %s", calendar, msg)
        self.display.clear()
        self.display.show_message(msg)

    def _handle_regular_day(self, calendar):
        sleeps = calendar.sleeps_to_next_event
        unit = 'sleeps' if sleeps > 1 else 'sleep'
        msg = "{} in {} {}".format(
            calendar.next_event, sleeps, unit)
        LOGGER.info(
            "Updating with calendar %s. Setting message to %s", calendar, msg)
        self.display.clear()
        self.display.show_message(msg)
        LOGGER.info("Setting message to %s", sleeps)
        self.display.show_message(str(sleeps))
