"""Mock and utilities for overriding the standard library datetime methods"""
import datetime
from unittest.mock import patch

def mock_datetime(target):
    """
    A utility function for patching the standard library datetime object with a
    mock. It may be used in a context manager as follows...

    today = datetime.datetime(
        year=2018,
        month=12,
        day=23,)

    with mock_datetime(target=today):
        CODE_UNDER_TEST

    Keyword arguments:
    target -- the datetime that you would like to be returned by mocks
    """
    class MockedDatetime(datetime.datetime):
        """
        A mock implemention of datetime used for patching datetime objects in
        tests
        """
        @classmethod
        def now(cls, tz=None):
            """Updates the target timezone info"""
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            """Returns the target datetime instance"""
            return target

        @classmethod
        def today(cls):
            """Returns the target datetime instance"""
            return target

    return patch.object(datetime, 'datetime', MockedDatetime)
