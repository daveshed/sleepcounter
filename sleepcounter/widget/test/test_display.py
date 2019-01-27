import datetime
import logging
import os
import sys
import unittest
from unittest.mock import Mock, patch, call

from sleepcounter.time.calendar import Calendar
from sleepcounter.time.event import SpecialDay
from sleepcounter.mocks.datetime import mock_datetime
from sleepcounter.widget.display import LedMatrixWidget

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=sys.stdout,
    level=logging.INFO)

CHRISTMAS_DAY = SpecialDay(name='Christmas', month=12, day=25,)
NEW_YEARS_DAY = SpecialDay(name="New Year\'s Day", month=1, day=1,)

def create_calendar():
    return (
        Calendar()
            .add_event(CHRISTMAS_DAY)
            .add_event(NEW_YEARS_DAY)
        )


class TestBase(unittest.TestCase):

    def setUp(self):
        self.mock_matrix = Mock()
        self.display = LedMatrixWidget(self.mock_matrix)
        self.calendar = create_calendar()

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
        expected_sleeps_xmas = 2
        expected_sleeps_new_year = 9
        with mock_datetime(target=today):
            self.display.update(self.calendar)
        self.assertTrue(call('Christmas in {} sleeps'.format(expected_sleeps_xmas))
            in self.mock_matrix.show_message.call_args_list)
        self.assertTrue(
            call('New Year\'s Day in {} sleeps'.format(expected_sleeps_new_year))
            in self.mock_matrix.show_message.call_args_list)

    def test_display_should_not_show_dates_past(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=27,
            hour=12,
            minute=10)
        expected_sleeps_new_year = 5
        with mock_datetime(target=today):
            self.display.update(self.calendar)
        self.assertTrue(
            call('New Year\'s Day in {} sleeps'.format(expected_sleeps_new_year))
            in self.mock_matrix.show_message.call_args_list)
        # no message about xmas only new years expected
        self.assertTrue(1, len(self.mock_matrix.show_message.call_args_list))

    def test_display_shows_one_sleep(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=24,
            hour=12,
            minute=10)
        expected_sleeps = 1
        with mock_datetime(target=today):
            self.display.update(self.calendar)
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
            self.display.update(self.calendar)
        self.mock_matrix.show_message.assert_called_with("It's Christmas!")
