import datetime
from unittest import mock
import unittest

from sleepcounter.time.calendar import Calendar
from sleepcounter.time.datelibrary import DateLibrary

# TODO: same date every year
BONFIRE_NIGHT = datetime.date(2018, 11, 5)
HALLOWEEN = datetime.date(2018, 10, 31)
CHRISTMAS_DAY = datetime.date(2018, 12, 25)

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

    return mock.patch.object(datetime, 'datetime', MockedDatetime)


class CalendarDateKeeping(unittest.TestCase):

    def test_sleeps_to_xmas(self):
        today = datetime.datetime(
            year=2018,
            month=12,
            day=23,
            hour=11,
            minute=23)
        with mock_datetime(target=today):
            date_library = DateLibrary({'xmas': CHRISTMAS_DAY})
            calendar = Calendar(date_library)
            self.assertEqual(2, calendar.sleeps_to_event('xmas'))

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
            date_library = DateLibrary({'xmas': CHRISTMAS_DAY})
            calendar = Calendar(date_library)
            self.assertEqual(seconds_expected, calendar.seconds_to_event('xmas'))

    def test_get_next_event_to_happen(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=14,
            hour=23,
            minute=1)
        with mock_datetime(target=today):
            date_library = DateLibrary(
                {
                    'bonfire_night': BONFIRE_NIGHT,
                    'halloween': HALLOWEEN
                }
            )
            calendar = Calendar(date_library)
            self.assertEqual('halloween', calendar.next_event)

    def test_todays_event_exists_after_wakup_time(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=31,
            hour=8)
        with mock_datetime(target=today):
            date_library = DateLibrary(
                {
                    'bonfire_night': BONFIRE_NIGHT,
                    'halloween': HALLOWEEN
                }
            )
            calendar = Calendar(date_library)
            self.assertTrue(calendar.special_day_today)
            self.assertEqual('halloween', calendar.todays_event)

    def test_no_event_before_wakup_time(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=31,
            hour=5,
            minute=0)
        with mock_datetime(target=today):
            date_library = DateLibrary(
                {
                    'bonfire_night': BONFIRE_NIGHT,
                    'halloween': HALLOWEEN
                }
            )
            calendar = Calendar(date_library)
            self.assertIsNone(calendar.todays_event)
            self.assertFalse(calendar.special_day_today)

    def test_today_not_a_special_day(self):
        today = datetime.datetime(2018, 10, 14)
        with mock_datetime(target=today):
            date_library = DateLibrary(
                {
                    'bonfire_night': BONFIRE_NIGHT,
                    'halloween': HALLOWEEN
                }
            )
            calendar = Calendar(date_library)
            self.assertFalse(calendar.special_day_today)

    def test_is_nighttime(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=14,
            hour=23,
            minute=1)
        with mock_datetime(target=today):
            date_library = DateLibrary(
                {
                    'bonfire_night': BONFIRE_NIGHT,
                    'halloween': HALLOWEEN
                }
            )   
            calendar = Calendar(date_library)
            self.assertTrue(calendar.is_nighttime)

    def test_is_not_daytime(self):
        today = datetime.datetime(
            year=2018,
            month=10,
            day=14,
            hour=11,
            minute=1)
        with mock_datetime(target=today):
            date_library = DateLibrary(
                {
                    'bonfire_night': BONFIRE_NIGHT,
                    'halloween': HALLOWEEN
                }
            )   
            calendar = Calendar(date_library)
            self.assertFalse(calendar.is_nighttime)