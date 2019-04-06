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
from sleepcounter.diary import CUSTOM_DIARY
from sleepcounter.display.display import LedMatrix
from sleepcounter.display.factory import DISPLAY
from sleepcounter.widget.display import LedMatrixWidget
from sleepcounter.widget.stage import SleepsStageWidget

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

CONTROLLER = Controller(CUSTOM_DIARY)
CONTROLLER.register_widget(
    LedMatrixWidget(LedMatrix(DISPLAY)))
CONTROLLER.register_widget(
    SleepsStageWidget(Stage.from_config(STAGE_CONFIG)))

while True:
    CONTROLLER.update_widgets()
    sleep(10)
