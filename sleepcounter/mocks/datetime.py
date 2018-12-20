import datetime
from unittest.mock import patch

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
