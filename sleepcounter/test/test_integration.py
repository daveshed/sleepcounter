import datetime
import logging
import unittest
from unittest.mock import Mock, patch

from sleepcounter.controller import Controller
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.datelibrary import DateLibrary
# from sleepcounter.widget.display import LedMatrixWidget
#################### patch gpio module before import ###########################
import sys
mock_gpio = Mock()
# This only seems to work in python 3.7
sys.modules['RPi.GPIO'] = mock_gpio
from sleepcounter.widget.stage import LinearStageWidget, MAX_STAGE_LIMIT
################################################################################

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=sys.stdout,
    level=logging.INFO)

CHRISTMAS_DAY = datetime.datetime(2018, 12, 25)
NEW_YEARS_DAY = datetime.datetime(2019, 1, 1)
CALENDAR = Calendar(DateLibrary(
    {
        'Christmas': CHRISTMAS_DAY,
        'New Years Day': NEW_YEARS_DAY,
    }
))


def mock_datetime(target):

    class MockedDatetime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return target

        @classmethod
        def today(cls):
            return target

    return patch.object(datetime, 'datetime', MockedDatetime)

class ControllerIntegrationLinearStage(unittest.TestCase):

    def setUp(self):
        self.controller = Controller(CALENDAR)
        self.stage = LinearStageWidget(
                motor=Mock(),
                end_stop=Mock()
            )
        self.controller.register_widget(self.stage)

    def test_linear_stage_updates_position(self):
        days_to_event = 10
        today = CHRISTMAS_DAY - datetime.timedelta(days=days_to_event)
        with mock_datetime(target=today):
            self.controller.update_widgets()
        self.assertEqual(0, self.stage.position)

        tomorrow = today + datetime.timedelta(days=1)
        with mock_datetime(target=tomorrow):
            self.controller.update_widgets()
        expected_position = 1 / 10 * MAX_STAGE_LIMIT
        self.assertEqual(expected_position, self.stage.position)
    
    #TODO: test for position updated as seconds elapse
