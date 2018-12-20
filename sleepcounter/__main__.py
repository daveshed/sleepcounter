from datetime import datetime
import logging
from sys import stdout
from time import sleep

from linearstage.config import STAGE_CONFIG
from sleepcounter.controller import Controller
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.datelibrary import DateLibrary
from sleepcounter.widget.display import LedMatrixWidget, create_default_display
from linearstage.stage import Stage
from sleepcounter.widget.stage import SleepsStageWidget

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

calendar = Calendar(DateLibrary(
    {
        'Christmas': datetime(2018, 12, 25).date(),
        'New Years Day': datetime(2019, 1, 1).date(),
    }
))
controller = Controller(calendar)
controller.register_widget(
    LedMatrixWidget(create_default_display()))
controller.register_widget(
    SleepsStageWidget(Stage.from_config(STAGE_CONFIG)))

while True:
    controller.update_widgets()
    sleep(60)