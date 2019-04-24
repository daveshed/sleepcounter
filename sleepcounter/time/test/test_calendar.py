import datetime
import logging
from unittest import mock
from sys import stdout
import unittest

from sleepcounter.mocks.datetime import mock_datetime
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.event import SpecialDay, Anniversary

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

BONFIRE_NIGHT = Anniversary(name='Bonfire Night', month=11, day=5,)
HALLOWEEN = Anniversary(name='Halloween', month=10, day=31,)
CHRISTMAS = Anniversary(name='xmas', month=12, day=25,)

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
            xmas = Anniversary(
                name='xmas',
                month=12,
                day=25)
            calendar = Calendar().add_event(xmas)
            self.assertEqual(2, calendar.sleeps_to_event(xmas))

    def test_sleeps_to_xmas_too_many_sleeps(self):
        # Events may have a configurable number of sleeps to count when passed
        # the (optional) sleeps kwarg on addition to the the calendar. Test that
        # if there are more sleeps to the event than configured, then the event
        # will not appear in the calendar: it's too far away so don't bother to
        # report it.
        xmas_day = 25
        sleeps_to_xmas = 23
        sleeps_to_count = 10
        today = datetime.datetime(
            year=2018,
            month=12,
            day=xmas_day - sleeps_to_xmas,
            hour=11,
            minute=23)
        with mock_datetime(target=today):
            xmas = Anniversary(
                name='xmas',
                month=12,
                day=xmas_day,
                sleeps=sleeps_to_count)
            calendar = create_calendar()
            calendar.add_event(xmas)
            self.assertNotIn(xmas, calendar.events)

    def test_non_recurring_event_with_sleeps_does_not_exist_after_seen(self):
        # Test that after a non-recurring event has happened we don't report it
        # any longer. Should be reported before the date but not after.
        today = datetime.datetime(
            year=2018,
            month=5,
            day=5,
            hour=9,
            minute=15)
        foo = SpecialDay(
            name='foo_event',
            year=2018,
            month=5,
            day=3,
            sleeps=10)
        calendar = create_calendar()
        calendar.add_event(foo)
        with mock_datetime(target=today):
            self.assertNotIn(foo, calendar.events)

    def test_non_recurring_event_without_sleeps_does_not_exist_after_seen(self):
        today = datetime.datetime(
            year=2018,
            month=5,
            day=5,
            hour=9,
            minute=15)
        foo = SpecialDay(
            name='foo_event',
            year=2018,
            month=5,
            day=3)
        calendar = create_calendar()
        calendar.add_event(foo)
        with mock_datetime(target=today):
            self.assertNotIn(foo, calendar.events)

    def test_non_recurring_event_exists_before_seen(self):
        # Test that before a non-recurring event has happened we do actually see
        # it in the calendar.
        today = datetime.datetime(
            year=2018,
            month=4,
            day=3,
            hour=9,
            minute=15)
        with mock_datetime(target=today):
            foo = SpecialDay(
                name='foo_event',
                year=2018,
                month=5,
                day=3)
            calendar = create_calendar()
            calendar.add_event(foo)
            self.assertIn(foo, calendar.events)

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
