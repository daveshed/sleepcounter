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
        self.display.clear()
        if calendar.special_day_today:
            self._handle_special_day(calendar)
        else:
            self._handle_regular_day(calendar)

    def _handle_special_day(self, calendar):
        msg = "It's {}!".format(calendar.todays_event)
        LOGGER.info(
            "Updating with calendar %s. Setting message to %s", calendar, msg)
        self.display.show_message(msg)

    def _handle_regular_day(self, calendar):
        # show all events in the calendar
        for event in calendar.date_library.events:
            sleeps = calendar.sleeps_to_event(event)
            if sleeps < 0:
                # ignore events in the past
                continue
            unit = 'sleeps' if sleeps > 1 else 'sleep'
            msg = "{} in {} {}".format(
                event, sleeps, unit)
            LOGGER.info(
                "Updating with calendar %s. Setting message to %s",
                calendar, msg)
            self.display.show_message(msg)
