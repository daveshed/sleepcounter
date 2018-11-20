from datetime import datetime
import logging
from sys import stdout
from time import sleep

from linearstage.config import (
    COIL_A1_PIN,
    COIL_A2_PIN,
    COIL_B1_PIN,
    COIL_B2_PIN,
    END_STOP_PIN,
    MIN_STAGE_LIMIT,
    MAX_STAGE_LIMIT,
    SEQUENCE,
)
from linearstage.endstop import EndStop
from linearstage.motor import Motor
from sleepcounter.controller import Controller
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.datelibrary import DateLibrary
from sleepcounter.widget.display import LedMatrixWidget
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
endstop = EndStop(END_STOP_PIN)
motor = Motor(
    pins=[
        COIL_A1_PIN,
        COIL_A2_PIN,
        COIL_B1_PIN,
        COIL_B2_PIN,
    ],
    sequence=SEQUENCE)
controller.register_widget(LinearStageWidget(motor, endstop))

while True:
    controller.update_widgets()
    sleep(60)