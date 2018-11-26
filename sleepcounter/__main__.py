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
from sleepcounter.widget.stage import LinearStageWidget

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

calendar = Calendar(DateLibrary(
    {
        'Christmas': datetime(2018, 12, 25),
        'New Years Day': datetime(2019, 1, 1),
    }
))
controller = Controller(calendar)
controller.register_widget(LedMatrixWidget())
controller.register_widget(
    LinearStageWidget(Stage.from_config(STAGE_CONFIG)))

while True:
    controller.update_widgets()
    sleep(60)