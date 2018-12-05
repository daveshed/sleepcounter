import logging
import json

from linearstage.stage import Stage
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
    def __init__(self, file=None):
        if file is None:
            self._file = DEFAULT_RECOVERY_FILE
        else:
            self._file = file
        LOGGER.info("instantiating {} with file".format(self, self._file))
        try:
            self.recover()
        except FileNotFoundError:
            LOGGER.warning("No recovery data. Creating a new file")
            self.record("")

    def record(self, data):
        with open(self._file, 'w') as fp:
            serialised = json.dumps(data)
            LOGGER.info("Writing %s to file", serialised)
            fp.write(serialised)

    def recover(self):
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


class LinearStageWidget(BaseWidget):
    """
    Represents the date using a linear translation stage. The stage moves along
    as the date nears an important event.
    """
    def __init__(self, stage, recovery_file=None):
        LOGGER.info("Instantiating %s", self)
        self._persistent_data = RecoveryData(recovery_file)
        recovered = self._persistent_data.recover()
        if recovered is None:
            self._total_seconds = None # call reset
        else:
            self._total_seconds, self._next_event = recovered
            LOGGER.info(
                "Counting %r seconds to event %s in total",
                self._total_seconds,
                self._next_event)
        self.stage = stage
        self.stage.home()

    def update(self, calendar):
        """
        Update the position of the stage based on the time to the event. If
        today i/s a special day, then restart the timer and don't move. Otherwise
        go home and scale the position based on the time remaining to the event.
        """
        LOGGER.info(
            "Updating with calendar {}".format(calendar))
        if calendar.special_day_today:
            LOGGER.info("Today is a special day. Moving stage to max position")
            self._total_seconds = None
            self.stage.end()
        else:
            if (self._total_seconds is None
                    or calendar.next_event != self._next_event):
                LOGGER.info("Setting initial time. Homing stage")
                self._next_event = calendar.next_event
                self._total_seconds = calendar.seconds_to_next_event
                self.stage.home()
                self._persistent_data.record((self._total_seconds, self._next_event,))
            else:
                seconds_done = \
                    (self._total_seconds - calendar.seconds_to_next_event)
                pos = int(seconds_done / self._total_seconds * self.stage.max)
                LOGGER.info("{} sec to next event. Updating position to {}"
                    .format(calendar.seconds_to_next_event, pos))
                self.stage.position = pos
