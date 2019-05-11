"""
Main entry-point module for the sleepcounter. All instances are created here
and the application is started.
"""
import logging
from sys import stdout
from time import sleep

from linearstage.config import STAGE_CONFIG
from linearstage.stage import Stage
from sleepcounter.application import Application
from sleepcounter.diary import CUSTOM_DIARY
from sleepcounter.display.display import LedMatrix
from sleepcounter.display.factory import DISPLAY
from sleepcounter.widget.display import LedMatrixWidget
from sleepcounter.widget.stage import SleepsStageWidget

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

def main():
    """Application main function. Instantiates some widgets and runs the app"""
    display_widget = LedMatrixWidget(
        display=LedMatrix(DISPLAY),
        calendar=CUSTOM_DIARY)
    stage_widget = SleepsStageWidget(
        stage=Stage.from_config(STAGE_CONFIG),
        calendar=CUSTOM_DIARY)
    app = Application(widgets=[display_widget, stage_widget])
    app.start()
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            app.stop()
            break

if __name__ == "__main__":
    main()
