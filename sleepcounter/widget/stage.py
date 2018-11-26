import logging

from linearstage.stage import Stage
from sleepcounter.widget.base import BaseWidget


LOGGER = logging.getLogger("stage widget")


class LinearStageWidget(BaseWidget):
    """
    Represents the date using a linear translation stage. The stage moves along
    as the date nears an important event.
    """
    def __init__(self, stage):
        LOGGER.info("Instantiating")
        self.stage = stage
        self.reset()

    def reset(self):
        self._total_seconds = None

    def update(self, calendar):
        """
        Update the position of the stage based on the time to the event. If
        today is a special day, then restart the timer and don't move. Otherwise
        go home and scale the position based on the time remaining to the event.
        """
        LOGGER.info(
            "Updating with calendar {}".format(calendar))
        if calendar.special_day_today:
            LOGGER.info("Today is a special day.")
            self.reset()
        else:
            if self._total_seconds is None:
                LOGGER.info("Setting initial time. Homing stage")
                self._total_seconds = calendar.seconds_to_next_event
                self.stage.home()
            else:
                seconds_done = \
                    (self._total_seconds - calendar.seconds_to_next_event)
                pos = int(seconds_done / self._total_seconds * self.stage._max)
                LOGGER.info("{} sec to next event. Updating position to {}"
                    .format(calendar.seconds_to_next_event, pos))
                self.stage.position = pos
