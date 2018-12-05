from unittest.mock import Mock, patch
import datetime
import logging
import os
import sys
import unittest
################# patch hardware specific modules before import ################
# This only seems to work in python 3.7
sys.modules['RPi.GPIO'] = Mock()
from sleepcounter.widget.stage import LinearStageWidget, DEFAULT_RECOVERY_FILE
################################################################################
from linearstage.stage import Stage, OutOfRangeError
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.datelibrary import DateLibrary

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=sys.stdout,
    level=logging.INFO)

JUST_BEFORE_XMAS = datetime.datetime(
    year=2018,
    month=12,
    day=3,
    hour=8,
    minute=5)
CHRISTMAS_DAY = datetime.datetime(year=2018, month=12, day=25)
NEW_YEARS_DAY = datetime.datetime(year=2019, month=1, day=1)
# have to enter dates into the calendar as datetime.date objects
CALENDAR = Calendar(DateLibrary(
    {
        'Christmas': CHRISTMAS_DAY.date(),
        'New Years Day': NEW_YEARS_DAY.date(),
    }
))

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

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


class MockStage:
    MAX_POS = 100
    MIN_POS = 0

    def __init__(self):
        self.home()

    def home(self):
        self._position = __class__.MIN_POS

    def end(self):
        self._position = self.max

    @property
    def max(self):
        return __class__.MAX_POS

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, request):
        too_large = request > __class__.MAX_POS
        too_small = request < __class__.MIN_POS
        if too_large or too_small:
            raise OutOfRangeError("Cannot go to position {}"
                .format(request))
        self._position = request


class TestBase(unittest.TestCase):

    def _clean_up_tmp_files(self):
        if os.path.exists(DEFAULT_RECOVERY_FILE):
            os.remove(DEFAULT_RECOVERY_FILE)
        if hasattr(self, 'recovery_file'):
            os.remove(self.recovery_file)        

    def setUp(self):
        self._clean_up_tmp_files()
        self.mock_stage = MockStage()

    def tearDown(self):
        self._clean_up_tmp_files()


class StageWidgetStoresPerisistentData(TestBase):
            
    def test_reinitialise_to_stored_position(self):
        self.recovery_file = DIR_PATH + '/tmp'
        stage_widget = LinearStageWidget(
            stage=self.mock_stage,
            recovery_file=self.recovery_file)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        today += datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        # store the position in the test before going down
        pos_before = self.mock_stage.position
        # system goes down which resets the stage, widget is reinitialised
        self.mock_stage = MockStage()
        stage_widget = LinearStageWidget(
            stage=self.mock_stage,
            recovery_file=self.recovery_file)
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        # get the position after restarting
        pos_after = self.mock_stage.position
        # the position should be same as before it went down
        self.assertEqual(pos_after, pos_before)

    def test_reinitialise_to_stored_position_default_file(self):
        stage_widget = LinearStageWidget(self.mock_stage)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        today += datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        # store the position in the test before going down
        pos_before = self.mock_stage.position
        # system goes down which resets the stage, widget is reinitialised
        self.mock_stage = MockStage()
        stage_widget = LinearStageWidget(
            stage=self.mock_stage)
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        # get the position after restarting
        pos_after = self.mock_stage.position
        # the position should be same as before it went down
        self.assertEqual(pos_after, pos_before)

    def test_reinitialised_after_event_should_reset(self):
        stage_widget = LinearStageWidget(self.mock_stage)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        today += datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        pos_before = self.mock_stage.position
        # system goes down which resets the stage, widget is reinitialised
        self.mock_stage = MockStage()
        stage_widget = LinearStageWidget(
            stage=self.mock_stage)
        # system is brought back up after an event so should restart counting
        today = CHRISTMAS_DAY + datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        # stage should home to restart counting
        self.assertEqual(0, self.mock_stage.position)


class StageWidgetDisplaysTime(TestBase):
    
    def test_stage_at_end_on_special_day(self):
        stage_widget = LinearStageWidget(self.mock_stage)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        today += datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        today = datetime.datetime(
            year=2018,
            month=12,
            day=25,
            hour=8,
            minute=12,
        )
        with mock_datetime(target=today):
            stage_widget.update(CALENDAR)
        self.assertEqual(MockStage.MAX_POS, self.mock_stage.position)
