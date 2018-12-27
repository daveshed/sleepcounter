import datetime
import logging
import os
import unittest
from unittest.mock import Mock, patch, call

from sleepcounter.time.calendar import Calendar, _WAKE_UP_TIME
from sleepcounter.time.datelibrary import DateLibrary
################# patch hardware specific modules before import ################
import sys
# # This only seems to work in python 3.7
sys.modules['max7219.led'] = Mock()
################################################################################
from sleepcounter.mocks.datetime import mock_datetime
from sleepcounter.widget.display import LedMatrixWidget

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=sys.stdout,
    level=logging.INFO)

CHRISTMAS_DAY = datetime.datetime(2018, 12, 25)
NEW_YEARS_DAY = datetime.datetime(2019, 1, 1)
CALENDAR = Calendar(DateLibrary(
    {
        'Christmas': CHRISTMAS_DAY.date(),
        'New Years Day': NEW_YEARS_DAY.date(),
    }
))


class TestBase(unittest.TestCase):

    def setUp(self):
        self.mock_matrix = Mock()
        self.display = LedMatrixWidget(self.mock_matrix)

    def tearDown(self):
        pass


class DisplayUpdateTests(TestBase):

    def test_display_shows_correct_sleeps(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=23,
            hour=12,
            minute=10)
        expected_sleeps = 2
        with mock_datetime(target=today):
            self.display.update(CALENDAR)
        self.mock_matrix.show_message.assert_called_with(str(expected_sleeps))
        self.assertTrue(call('Christmas in {} sleeps'.format(expected_sleeps))
            in self.mock_matrix.show_message.call_args_list)

    def test_display_shows_one_sleep(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=24,
            hour=12,
            minute=10)
        expected_sleeps = 1
        with mock_datetime(target=today):
            self.display.update(CALENDAR)
        self.mock_matrix.show_message.assert_called_with(str(expected_sleeps))
        self.assertTrue(call('Christmas in 1 sleep') in 
            self.mock_matrix.show_message.call_args_list)

    def test_display_shows_special_day(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=25,
            hour=17,
            minute=9)
        with mock_datetime(target=today):
            self.display.update(CALENDAR)
        self.mock_matrix.show_message.assert_called_with("It's Christmas!")
