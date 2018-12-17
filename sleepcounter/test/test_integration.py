import datetime
import logging
import os
import unittest
from unittest.mock import Mock, patch, call

from linearstage.config import STAGE_CONFIG
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
################################################################################
from sleepcounter.test.utils import MockStage, mock_datetime
from sleepcounter.widget.display import LedMatrixWidget
from sleepcounter.widget.stage import (
    SecondsStageWidget,
    SleepsStageWidget,
    DEFAULT_RECOVERY_FILE)

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
MAX_STAGE_LIMIT = STAGE_CONFIG['max_limit']


class TestBase(unittest.TestCase):

    def _clean_up_tmp_files(self):
        if os.path.exists(DEFAULT_RECOVERY_FILE):
            os.remove(DEFAULT_RECOVERY_FILE)

    def setUp(self):
        self._clean_up_tmp_files()
        mock_led.reset_mock()
        mock_matrix.reset_mock()
        self.controller = Controller(CALENDAR)
        self.linearstage = MockStage()
        self.display = LedMatrixWidget()
        self.controller.register_widget(self.display)

    def tearDown(self):
        self._clean_up_tmp_files()


class IntegrationSecondCounterWithDisplay(TestBase):

    def setUp(self):
        super().setUp()
        self.controller.register_widget(
            SecondsStageWidget(stage=self.linearstage))

    def test_linear_stage_updates_position(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=23,
            hour=12,
            minute=10)
        with mock_datetime(target=today):
            self.controller.update_widgets()
        self.assertEqual(MockStage.MIN_POS, self.linearstage.position)
        deadline = datetime.datetime.combine(CHRISTMAS_DAY, _WAKE_UP_TIME)
        time_to_event = deadline - today
        time_elapsed = datetime.timedelta(days=1)
        tomorrow = today + time_elapsed
        with mock_datetime(target=tomorrow):
            self.controller.update_widgets()
        expected_position = \
            int(time_elapsed / time_to_event * MockStage.MAX_POS)
        self.assertEqual(expected_position, self.linearstage.position)

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


class IntegrationSleepsCounterWithDisplay(TestBase):

    def setUp(self):
        super().setUp()
        self.controller.register_widget(
            SleepsStageWidget(stage=self.linearstage))

    def test_linear_stage_updates_position(self):
        reset_time = datetime.datetime(
            year=2018,
            month=12,
            day=23,
            hour=12,
            minute=10)
        with mock_datetime(target=reset_time):
            self.controller.update_widgets()
        # stage should reset and move to minimum position
        self.assertEqual(MockStage.MIN_POS, self.linearstage.position)
        expected_sleeps = 2
        # another sleep elapses
        sleeps_elapsed = 1
        tomorrow = reset_time + datetime.timedelta(days=1)
        with mock_datetime(target=tomorrow):
            self.controller.update_widgets()
        expected_position = \
            int(sleeps_elapsed / expected_sleeps * MockStage.MAX_POS)
        self.assertEqual(expected_position, self.linearstage.position)

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
