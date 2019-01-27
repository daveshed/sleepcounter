"""Configuration constants defining wake-up time and bedtime"""
import datetime


class SleepChecker:
    """Checks whether it's nighttime and returns the result as a bool"""
    # pylint: disable=too-few-public-methods
    WAKE_UP_TIME = datetime.time(
        hour=6,
        minute=30,
        second=0)
    BEDTIME = datetime.time(
        hour=19,
        minute=0,
        second=0)

    @staticmethod
    def is_nighttime():
        """Returns a bool to indicate whether it's nighttime"""
        now = datetime.datetime.now().time()
        return now > __class__.BEDTIME or now < __class__.WAKE_UP_TIME
