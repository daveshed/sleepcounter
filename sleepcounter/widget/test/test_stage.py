from unittest.mock import Mock, patch
import datetime
import logging
import os
import sys
import unittest
################# patch hardware specific modules before import ################
# This only seems to work in python 3.7
sys.modules['RPi.GPIO'] = Mock()
from sleepcounter.widget.stage import (
    SecondsStageWidget,
    SleepsStageWidget,
    DEFAULT_RECOVERY_FILE)
################################################################################

from sleepcounter.mocks.datetime import mock_datetime
from sleepcounter.mocks.stage import MockStage
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.event import Anniversary

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

CHRISTMAS_DAY = Anniversary(name='xmas', month=12, day=25,)
NEW_YEARS_DAY = Anniversary(name="New Year\'s Day", month=1, day=1,)

def create_calendar():
    return (
        Calendar()
            .add_event(CHRISTMAS_DAY)
            .add_event(NEW_YEARS_DAY)
        )

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ALTERNATIVE_FILE_PATH = DIR_PATH + '/tmp'


class TestBase(unittest.TestCase):

    def _clean_up_tmp_files(self):
        if os.path.exists(DEFAULT_RECOVERY_FILE):
            os.remove(DEFAULT_RECOVERY_FILE)
        if os.path.exists(ALTERNATIVE_FILE_PATH):
            os.remove(ALTERNATIVE_FILE_PATH)

    def setUp(self):
        self._clean_up_tmp_files()
        self.mock_stage = MockStage()
        self.calendar = create_calendar()

    def tearDown(self):
        self._clean_up_tmp_files()


class StageWidgetStoresPerisistentData(TestBase):
            
    def test_reinitialise_to_stored_position(self):
        self.recovery_file = ALTERNATIVE_FILE_PATH
        stage_widget = SecondsStageWidget(
            stage=self.mock_stage,
            recovery_file=self.recovery_file)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        today += datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        # store the position in the test before going down
        pos_before = self.mock_stage.position
        # system goes down which resets the stage, widget is reinitialised
        self.mock_stage = MockStage()
        stage_widget = SecondsStageWidget(
            stage=self.mock_stage,
            recovery_file=self.recovery_file)
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        # get the position after restarting
        pos_after = self.mock_stage.position
        # the position should be same as before it went down
        self.assertEqual(pos_after, pos_before)

    def test_reinitialise_to_stored_position_default_file(self):
        stage_widget = SecondsStageWidget(self.mock_stage)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        today += datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        # store the position in the test before going down
        pos_before = self.mock_stage.position
        # system goes down which resets the stage, widget is reinitialised
        self.mock_stage = MockStage()
        stage_widget = SecondsStageWidget(
            stage=self.mock_stage)
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        # get the position after restarting
        pos_after = self.mock_stage.position
        # the position should be same as before it went down
        self.assertEqual(pos_after, pos_before)

    def test_reinitialised_after_event_should_reset(self):
        stage_widget = SecondsStageWidget(self.mock_stage)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        today += datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        pos_before = self.mock_stage.position
        # system goes down which resets the stage, widget is reinitialised
        self.mock_stage = MockStage()
        stage_widget = SecondsStageWidget(
            stage=self.mock_stage)
        # system is brought back up after an event so should restart counting
        just_after_christmas = datetime.datetime(
            year=2018,
            month=12,
            day=26,
            hour=7,
            minute=55)
        with mock_datetime(target=just_after_christmas):
            stage_widget.update(self.calendar)
        # stage should home to restart counting
        self.assertEqual(0, self.mock_stage.position)


class StageWidgetDisplaysTime(TestBase):
    
    def test_stage_at_end_on_special_day(self):
        stage_widget = SecondsStageWidget(self.mock_stage)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        today += datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        today = datetime.datetime(
            year=2018,
            month=12,
            day=25,
            hour=8,
            minute=12,
        )
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        self.assertEqual(MockStage.MAX_POS, self.mock_stage.position)


class SleepsStageWidgetDisplaysTime(TestBase):

    def test_stage_at_end_on_special_day(self):
        stage_widget = SleepsStageWidget(self.mock_stage)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        today += datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        today = datetime.datetime(
            year=2018,
            month=12,
            day=25,
            hour=8,
            minute=12,
        )
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        self.assertEqual(MockStage.MAX_POS, self.mock_stage.position)
        # a bit more timme passes but the widget should not move
        today = datetime.datetime(
            year=2018,
            month=12,
            day=25,
            hour=10,
            minute=7,
        )
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        self.assertEqual(MockStage.MAX_POS, self.mock_stage.position)

    def test_stage_homed_after_special_day(self):
        stage_widget = SleepsStageWidget(self.mock_stage)
        today = JUST_BEFORE_XMAS
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        xmas_day = datetime.datetime(
            year=2018,
            month=12,
            day=25,
            hour=8,
            minute=12,
        )
        with mock_datetime(target=xmas_day):
            stage_widget.update(self.calendar)
        today = xmas_day + datetime.timedelta(days=1)
        with mock_datetime(target=today):
            stage_widget.update(self.calendar)
        self.assertEqual(MockStage.MIN_POS, self.mock_stage.position)

    def test_stage_moves_forward_after_sleep(self):
        stage_widget = SleepsStageWidget(self.mock_stage)
        just_before_bedtime = datetime.datetime(
            year=2018,
            month=12,
            day=3,
            hour=18,
            minute=5)
        with mock_datetime(target=just_before_bedtime):
            stage_widget.update(self.calendar)
        # stage should be homed initially
        self.assertEqual(MockStage.MIN_POS, self.mock_stage.position)
        just_after_bedtime = datetime.datetime(
            year=2018,
            month=12,
            day=3,
            hour=21,
            minute=19)
        # stage should not move yet.
        with mock_datetime(target=just_after_bedtime):
            stage_widget.update(self.calendar)
        self.assertEqual(MockStage.MIN_POS, self.mock_stage.position)
        wake_up_time = datetime.datetime(
            year=2018,
            month=12,
            day=4,
            hour=8,
            minute=1)
        # stage should have moved now.
        with mock_datetime(target=wake_up_time):
            stage_widget.update(self.calendar)
        self.assertGreater(self.mock_stage.position, MockStage.MIN_POS)