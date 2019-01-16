"""Implementation for the stage widget that displays the number of seconds or
sleeps to the next event in therms of the distance from the end of the track"""
# pylint: disable=invalid-name
import json
import logging

from sleepcounter.widget.base import BaseWidget

LOGGER = logging.getLogger("stage widget")

DEFAULT_RECOVERY_PATH = '/var/tmp/'
DEFAULT_FILENAME = 'sleepcounter.tmp'
DEFAULT_RECOVERY_FILE = DEFAULT_RECOVERY_PATH + DEFAULT_FILENAME


class RecoveryData:
    """
    Recovers data from a file. Attributes written to the instance will be rec-
    orded to the file. When the instance is created, the same attributes are
    read from the file and overwritten if set again.
    """
    def __init__(self, file: str):
        """Create an instance using the filename specified."""
        self._file = file
        LOGGER.info("instantiating %s with file %s", self, self._file)

    def record(self, data):
        """serialise the data and save to file"""
        with open(self._file, 'w') as fp:
            serialised = json.dumps(data)
            LOGGER.info("Writing %s to file %s", serialised, self._file)
            fp.write(serialised)

    def recover(self):
        """recover data from the file"""
        contents = None
        try:
            contents = self._read()
        except FileNotFoundError:
            LOGGER.warning("No recovery data found.")
        return contents

    def _read(self):
        LOGGER.info("Getting saved data...")
        with open(self._file) as fp:
            contents = json.load(fp)
            LOGGER.info("Read %r from file", contents)
            return contents


class StageWidgetBase(BaseWidget):
    # pylint: disable=too-few-public-methods
    """
    Represents the date using a linear translation stage. The stage moves along
    as the date nears an important event.
    """
    units = None

    def __init__(self, stage, recovery_file=DEFAULT_RECOVERY_FILE):
        LOGGER.info("Instantiating %s", self)
        self._persistent_data = RecoveryData(recovery_file)
        recovered = self._persistent_data.recover()
        if recovered is None:
            self._total_time = None
            self._next_event = None
        else:
            self._total_time, self._next_event = recovered
            LOGGER.info(
                "Counting %r %s to event %s in total",
                self._total_time,
                self.units,
                self._next_event)
        self.stage = stage
        self.stage.home()

    def update(self, calendar):
        """
        Update the position of the stage based on the time to the event. If
        today i/s a special day, then restart the timer and don't move. Otherwise
        go home and scale the position based on the time remaining to the event.
        """
        LOGGER.info("Updating with calendar %s", calendar)
        if calendar.special_day_today:
            LOGGER.info("Today is a special day. Moving stage to end position")
            self._total_time = None
            self.stage.end()
        else:
            if (self._total_time is None
                    or calendar.next_event != self._next_event):
                LOGGER.info("Setting initial time. Homing stage")
                self._next_event = calendar.next_event
                self._total_time = self._get_time_to_next_event(calendar)
                self.stage.home()
                self._persistent_data.record(
                    (self._total_time, self._next_event,))
            else:
                time_done = \
                    (self._total_time - self._get_time_to_next_event(calendar))
                pos = int(time_done / self._total_time * self.stage.max)
                LOGGER.info(
                    "%r %s to next event. Updating position to %d",
                    self._get_time_to_next_event(calendar),
                    self.units,
                    pos,
                )
                self.stage.position = pos

    @staticmethod
    def _get_time_to_next_event(calendar):
        raise NotImplementedError


class SecondsStageWidget(StageWidgetBase):
    # pylint: disable=too-few-public-methods
    """
    Represents the date using a linear translation stage. The stage moves along
    as the date nears an important event tracking the number of seconds elapsed.
    """
    units = "seconds"

    @staticmethod
    def _get_time_to_next_event(calendar):
        return calendar.seconds_to_next_event


class SleepsStageWidget(StageWidgetBase):
    # pylint: disable=too-few-public-methods
    """
    Represents the date using a linear translation stage. The stage moves along
    as the date nears an important event tracking the number of sleeps elapsed.
    """
    units = "sleeps"

    @staticmethod
    def _get_time_to_next_event(calendar):
        return calendar.sleeps_to_next_event
