from datetime import datetime
import logging
from sys import stdout
from time import sleep

from linearstage.config import STAGE_CONFIG
from sleepcounter.controller import Controller
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.datelibrary import DateLibrary
from sleepcounter.widget.display import LedMatrixWidget
from linearstage.stage import Stage
from sleepcounter.widget.stage import SleepsStageWidget

from sleepcounter.display.factory import DISPLAY
from sleepcounter.display.display import LedMatrix

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

calendar = Calendar(DateLibrary(
    {
        'Christmas': datetime(2018, 12, 25).date(),
        'New Years Day': datetime(2019, 1, 1).date(),
        'Daddy\'s Birthday': datetime(2019, 1, 25).date(),
        'Jesse\'s Birthday': datetime(2019, 2, 12).date(),
        'Totty\'s Birthday': datetime(2019, 2, 14).date(),
    }
))
controller = Controller(calendar)
controller.register_widget(
    LedMatrixWidget(LedMatrix(DISPLAY)))
controller.register_widget(
    SleepsStageWidget(Stage.from_config(STAGE_CONFIG)))

while True:
    controller.update_widgets()
    sleep(10)