from datetime import datetime
from time import sleep

from sleepcounter.controller import Controller
from sleepcounter.time.calendar import Calendar
from sleepcounter.time.datelibrary import DateLibrary
from sleepcounter.widget.display import LedMatrixWidget
from sleepcounter.widget.stage import LinearStageWidget


calendar = Calendar(DateLibrary(
    {
        'Christmas': datetime(2018, 1, 25),
        'New Years Day': datetime(2019, 1, 1),
    }
))
controller = Controller(calendar)
controller.register_widget(LedMatrixWidget())
controller.register_widget(LinearStageWidget())

while True:
    controller.update_widgets()
    sleep(60)