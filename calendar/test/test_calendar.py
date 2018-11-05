import datetime
from unittest import mock
import unittest

from calendar import Calendar
from calendar import DateLibrary

# TODO: same date every year
BONFIRE_NIGHT = datetime.datetime(2018, 11, 5)
HALLOWEEN = datetime.datetime(2018, 10, 31)
CHRISTMAS_DAY = datetime.datetime(2018, 12, 25)

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

    def test_days_to_xmas(self):
        today = datetime.datetime(2018, 12, 23)
        with mock_datetime(target=today):
            date_library = DateLibrary({'foo': CHRISTMAS_DAY})
            calendar = Calendar(date_library)
            self.assertEqual(2, calendar.days_to_event('foo'))

    def test_next_event_to_happen(self):
        today = datetime.datetime(2018, 10, 14)
        with mock_datetime(target=today):
            date_library = DateLibrary(
                {
                    'bonfire_night': BONFIRE_NIGHT,
                    'halloween': HALLOWEEN
                }
            )
            calendar = Calendar(date_library)
            self.assertEqual('halloween', calendar.next_event)
            self.assertEqual(17, calendar.days_to_next_event)

    def test_todays_event_exists(self):
        today = datetime.datetime(2018, 10, 31)
        with mock_datetime(target=today):
            date_library = DateLibrary(
                {
                    'bonfire_night': BONFIRE_NIGHT,
                    'halloween': HALLOWEEN
                }
            )
            calendar = Calendar(date_library)
            self.assertEqual('halloween', calendar.todays_event)

    def test_todays_event_does_not_exist(self):
        today = datetime.datetime(2018, 10, 14)
        with mock_datetime(target=today):
            date_library = DateLibrary(
                {
                    'bonfire_night': BONFIRE_NIGHT,
                    'halloween': HALLOWEEN
                }
            )
            calendar = Calendar(date_library)
            self.assertIsNone(calendar.todays_event)

