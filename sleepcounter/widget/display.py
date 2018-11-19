import logging

from max7219 import led

from sleepcounter.widget.base import BaseWidget


LOGGER = logging.getLogger("display widget") 

class LedMatrixWidget(BaseWidget, led.matrix):
    """
    Represents the date using an led matrix. 
    """
    def __init__(self):
        LOGGER.info("Intantiating")
        led.matrix.__init__(cascaded=4)
        self._spi.max_speed_hz = 7800000
        self.orientation(90)
        self.brightness(2)
        self.clear()
        
    def update(self, calendar):
        msg = "{} in {} sleeps".format(
            calendar.next_event, calendar.days_to_next_event)
        LOGGER.info(
            "Updating with calendar {}. Setting message to {}"
            .format(calendar, msg))
        self.show_message(msg)