"""
Main entry-point module for the sleepcounter. All instances are created here
and the application is started.
"""
from datetime import datetime
import logging
from sys import stdout
from time import sleep

from linearstage.config import STAGE_CONFIG
from linearstage.stage import Stage
from sleepcounter.controller import Controller
from sleepcounter.display.display import LedMatrix
from sleepcounter.display.factory import DISPLAY
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.datelibrary import DateLibrary
from sleepcounter.widget.display import LedMatrixWidget
from sleepcounter.widget.stage import SleepsStageWidget

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

CALENDAR = Calendar(DateLibrary(
    {
        'Christmas': datetime(2018, 12, 25).date(),
        'New Years Day': datetime(2019, 1, 1).date(),
        'Daddy\'s Birthday': datetime(2019, 1, 25).date(),
        'Jesse\'s Birthday': datetime(2019, 2, 12).date(),
        'Totty\'s Birthday': datetime(2019, 2, 14).date(),
    }
))
CONTROLLER = Controller(CALENDAR)
CONTROLLER.register_widget(
    LedMatrixWidget(LedMatrix(DISPLAY)))
CONTROLLER.register_widget(
    SleepsStageWidget(Stage.from_config(STAGE_CONFIG)))

while True:
    CONTROLLER.update_widgets()
    sleep(10)
