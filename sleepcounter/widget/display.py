import logging

from max7219 import led

from sleepcounter.widget.base import BaseWidget


LOGGER = logging.getLogger("display widget") 

display = led.matrix(cascaded=4)
display._spi.max_speed_hz = 7800000
display = led.matrix(cascaded=4)
display.orientation(90)
display.brightness(1)
display.clear()
display.show_message('READY!')


class LedMatrixWidget(BaseWidget):
    """
    Represents the date using an led matrix. 
    """
    def __init__(self):
        LOGGER.info("Intantiating")
        # led.matrix.__init__(self, cascaded=4)
        # led.matrix._spi.max_speed_hz = 7800000
        # self.orientation(90)
        # self.brightness(2)
        # self.clear()
        
    def update(self, calendar):
        msg = "{} in {} sleeps".format(
            calendar.next_event, calendar.days_to_next_event)
        LOGGER.info(
            "Updating with calendar {}. Setting message to {}"
            .format(calendar, msg))
        display.show_message(msg)
        LOGGER.info("Setting message to {}".format(calendar.days_to_next_event))
        display.show_message(
            str(calendar.days_to_next_event))