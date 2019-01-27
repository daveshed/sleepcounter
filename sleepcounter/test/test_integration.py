import datetime
import logging
import os
import unittest
from unittest.mock import Mock, patch, call

from linearstage.config import STAGE_CONFIG
from sleepcounter.controller import Controller
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.event import SpecialDay
from sleepcounter.time.bedtime import SleepChecker
################# patch hardware specific modules before import ################
import sys
# This only seems to work in python 3.7
sys.modules['RPi.GPIO'] = Mock()
sys.modules['max7219.led'] = Mock()
################################################################################
from sleepcounter.mocks.stage import MockStage
from sleepcounter.mocks.datetime import mock_datetime
from sleepcounter.widget.display import LedMatrixWidget
from sleepcounter.widget.stage import (
    SecondsStageWidget,
    SleepsStageWidget,
    DEFAULT_RECOVERY_FILE)

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=sys.stdout,
    level=logging.INFO)

BONFIRE_NIGHT = SpecialDay(name='Bonfire Night', month=11, day=5,)
HALLOWEEN = SpecialDay(name='Halloween', month=10, day=31,)
CHRISTMAS = SpecialDay(name='Christmas', month=12, day=25,)

def create_calendar():
    return (
        Calendar()
            .add_event(BONFIRE_NIGHT)
            .add_event(HALLOWEEN)
            .add_event(CHRISTMAS)
        )

MAX_STAGE_LIMIT = STAGE_CONFIG['max_limit']


class TestBase(unittest.TestCase):

    def _clean_up_tmp_files(self):
        if os.path.exists(DEFAULT_RECOVERY_FILE):
            os.remove(DEFAULT_RECOVERY_FILE)

    def setUp(self):
        self._clean_up_tmp_files()
        self.mock_matrix = Mock()
        self.calendar = create_calendar()
        self.controller = Controller(self.calendar)
        self.linearstage = MockStage()
        self.display = LedMatrixWidget(self.mock_matrix)
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
        # stage should home first
        self.assertEqual(MockStage.MIN_POS, self.linearstage.position)
        xmas = datetime.date(year=2018, month=12, day=25)
        deadline = datetime.datetime.combine(xmas, SleepChecker.WAKE_UP_TIME)
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
        with mock_datetime(target=today):
            self.controller.update_widgets()
        self.assertTrue(call('Christmas in 2 sleeps') in 
            self.mock_matrix.show_message.call_args_list)


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
        with mock_datetime(target=today):
            self.controller.update_widgets()
        self.assertTrue(call('Christmas in 2 sleeps') in 
            self.mock_matrix.show_message.call_args_list)
