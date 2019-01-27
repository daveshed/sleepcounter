"""
Main entry-point module for the sleepcounter. All instances are created here
and the application is started.
"""
import logging
from sys import stdout
from time import sleep

from linearstage.config import STAGE_CONFIG
from linearstage.stage import Stage
from sleepcounter.controller import Controller
from sleepcounter.display.display import LedMatrix
from sleepcounter.display.factory import DISPLAY
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.event import SpecialDay
from sleepcounter.widget.display import LedMatrixWidget
from sleepcounter.widget.stage import SleepsStageWidget

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

# BONFIRE_NIGHT = SpecialDay(name='Bonfire Night', month=11, day=5,)
# HALLOWEEN = SpecialDay(name='Halloween', month=10, day=31,)
CHRISTMAS = SpecialDay(name='Christmas', month=12, day=25,)
EVIES_BIRTHDAY = SpecialDay(name='Evie\'s Birthday', month=8, day=3,)
FELIXS_BIRTHDAY = SpecialDay(name='Felix\'s Birthday', month=6, day=16,)
LEGOLAND = SpecialDay(name='Legoland', month=4, day=27,)
TENERIFE = SpecialDay(name='Tenerife', month=2, day=19,)
TOTTYS_PARTY = SpecialDay(name='Totty\'s Party', month=2, day=16,)


CALENDAR = (
    Calendar()
        .add_event(CHRISTMAS)
        .add_event(EVIES_BIRTHDAY)
        .add_event(FELIXS_BIRTHDAY)
        .add_event(LEGOLAND)
        .add_event(TENERIFE)
        .add_event(TOTTYS_PARTY)
)
CONTROLLER = Controller(CALENDAR)
CONTROLLER.register_widget(
    LedMatrixWidget(LedMatrix(DISPLAY)))
CONTROLLER.register_widget(
    SleepsStageWidget(Stage.from_config(STAGE_CONFIG)))

while True:
    CONTROLLER.update_widgets()
    sleep(10)
