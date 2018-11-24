import datetime
import logging
import unittest
from unittest.mock import Mock, patch

from sleepcounter.controller import Controller
from sleepcounter.time.calendar import Calendar, _WAKE_UP_TIME
from sleepcounter.time.datelibrary import DateLibrary
################# patch hardware specific modules before import ################
import sys
mock_led = Mock()
mock_matrix = Mock()
mock_led.matrix = Mock(return_value=mock_matrix)
# This only seems to work in python 3.7
sys.modules['RPi.GPIO'] = Mock()
sys.modules['max7219.led'] = mock_led
from sleepcounter.widget.display import LedMatrixWidget
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


class ControllerIntegration(unittest.TestCase):

    def setUp(self):
        mock_led.reset_mock()
        mock_matrix.reset_mock()
        self.controller = Controller(CALENDAR)
        self.stage = LinearStageWidget(
                motor=Mock(),
                end_stop=Mock()
            )
        self.controller.register_widget(self.stage)
        self.display = LedMatrixWidget()
        self.controller.register_widget(self.display)

    def test_linear_stage_updates_position(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=23,
            hour=12,
            minute=10)
        with mock_datetime(target=today):
            self.controller.update_widgets()
        self.assertEqual(0, self.stage.position)
        deadline = datetime.datetime.combine(CHRISTMAS_DAY, _WAKE_UP_TIME)
        time_to_event = deadline - today
        time_elapsed = datetime.timedelta(days=1)
        tomorrow = today + time_elapsed
        with mock_datetime(target=tomorrow):
            self.controller.update_widgets()
        expected_position = \
            int(time_elapsed / time_to_event * MAX_STAGE_LIMIT)
        self.assertEqual(expected_position, self.stage.position)

    def test_led_matrix_updates_display(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=23,
            hour=12,
            minute=10)
        expected_sleeps = 2
        with mock_datetime(target=today):
            self.controller.update_widgets()
        mock_matrix.show_message.assert_called_with(str(expected_sleeps))
        