import datetime
import logging
from unittest import mock
from sys import stdout
import unittest

from sleepcounter.mocks.datetime import mock_datetime
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.event import SpecialDay

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

BONFIRE_NIGHT = SpecialDay(name='Bonfire Night', month=11, day=5,)
HALLOWEEN = SpecialDay(name='Halloween', month=10, day=31,)
CHRISTMAS = SpecialDay(name='xmas', month=12, day=25,)

def create_calendar():
    return (
        Calendar()
            .add_event(BONFIRE_NIGHT)
            .add_event(HALLOWEEN)
        )

class CalendarDateKeeping(unittest.TestCase):

    def test_sleeps_to_xmas(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=23,
            hour=11,
            minute=23)
        with mock_datetime(target=today):
            xmas = SpecialDay(
                name='xmas',
                month=12,
                day=25)
            calendar = Calendar().add_event(xmas)
            self.assertEqual(2, calendar.sleeps_to_event(xmas))

    def test_seconds_to_xmas(self):
        # set the time to wakup time two days before xmas
        days_expected = 2
        seconds_per_day = 24 * 3600
        seconds_expected = days_expected * seconds_per_day
        today = datetime.datetime(
            year=2018,
            month=12,
            day=23,
            hour=6,
            minute=30)
        with mock_datetime(target=today):
            calendar = Calendar().add_event(CHRISTMAS)
            self.assertEqual(
                seconds_expected,
                calendar.seconds_to_event(CHRISTMAS))

    def test_get_next_event_to_happen(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=14,
            hour=23,
            minute=1)
        with mock_datetime(target=today):
            calendar = create_calendar()
            self.assertEqual(HALLOWEEN, calendar.next_event)

    def test_todays_event_exists_after_wakeup_time(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=31,
            hour=8)
        with mock_datetime(target=today):
            calendar = create_calendar()
            self.assertTrue(calendar.special_day_today)
            self.assertEqual(HALLOWEEN, calendar.todays_event)

    def test_no_event_before_wakeup_time(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=31,
            hour=5,
            minute=0)
        with mock_datetime(target=today):
            calendar = create_calendar()
            self.assertIsNone(calendar.todays_event)
            self.assertFalse(calendar.special_day_today)

    def test_today_not_a_special_day(self):
        today = datetime.datetime(2018, 10, 14)
        with mock_datetime(target=today):
            calendar = create_calendar()
            self.assertFalse(calendar.special_day_today)

    def test_is_nighttime(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=14,
            hour=23,
            minute=1)
        with mock_datetime(target=today):
            calendar = create_calendar()
            self.assertTrue(calendar.is_nighttime)

    def test_is_not_daytime(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=14,
            hour=11,
            minute=1)
        with mock_datetime(target=today):
            calendar = create_calendar()
            self.assertFalse(calendar.is_nighttime)
