import logging

from max7219.led import matrix

from sleepcounter.widget.base import BaseWidget


LOGGER = logging.getLogger("display widget") 


display = matrix(cascaded=4)
# we need to create display then set speed and then recreate so that spped is
# correct when needed.# better would be to create the spi instance and pass this
# into the constructor to instantiate matrix
display._spi.max_speed_hz = 7800000
display = matrix(cascaded=4)
display.orientation(90)
display.brightness(2)
display.clear()
display.show_message('Ready')


class LedMatrixWidget(BaseWidget):
    """
    Represents the date using an led matrix. 
    """
    def __init__(self):
        LOGGER.info("Intantiating")
        
    def update(self, calendar):
        sleeps = calendar.sleeps_to_next_event
        msg = "{} in {} sleeps".format(
            calendar.next_event, sleeps)
        LOGGER.info(
            "Updating with calendar {}. Setting message to {}"
            .format(calendar, msg))
        display.clear()       
        display.show_message(msg)
        LOGGER.info("Setting message to {}".format(sleeps))
        display.show_message(str(sleeps))