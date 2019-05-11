import datetime
import logging
import os
import sys
from time import sleep
import unittest
from unittest.mock import Mock, patch, call

from sleepcounter.time.calendar import Calendar
from sleepcounter.time.event import Anniversary
from sleepcounter.mocks.datetime import mock_datetime
from sleepcounter.widget.display import LedMatrixWidget

CHRISTMAS_DAY = Anniversary(name='Christmas', month=12, day=25,)
NEW_YEARS_DAY = Anniversary(name="New Year\'s Day", month=1, day=1,)
CALENDAR = Calendar([CHRISTMAS_DAY, NEW_YEARS_DAY])
WIDGET_UPDATE_WAIT_SEC = 1


class TestBase(unittest.TestCase):

    def setUp(self):
        self.mock_matrix = Mock()
        self.display_widget = LedMatrixWidget(self.mock_matrix, CALENDAR)
        self.display_widget.start()

    def tearDown(self):
        self.display_widget.stop()


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
            sleep(WIDGET_UPDATE_WAIT_SEC)
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
            sleep(WIDGET_UPDATE_WAIT_SEC)
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
            sleep(WIDGET_UPDATE_WAIT_SEC)
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
            sleep(WIDGET_UPDATE_WAIT_SEC)
        self.mock_matrix.show_message.assert_called_with("It's Christmas!")
