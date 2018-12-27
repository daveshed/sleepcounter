import logging

from max7219.led import matrix

from sleepcounter.widget.base import BaseWidget


LOGGER = logging.getLogger("display widget") 

def create_default_display():
    display = matrix(cascaded=4)
    # we need to create display then set speed and then recreate so that spped
    # is correct when needed.# better would be to create the spi instance and
    # pass this into the constructor to instantiate matrix
    display._spi.max_speed_hz = 7800000
    display = matrix(cascaded=4)
    display.orientation(90)
    display.brightness(2)
    display.clear()
    display.show_message('Ready')
    return display


class LedMatrixWidget(BaseWidget):
    """
    Represents the date using an led matrix. 
    """
    def __init__(self, display):
        LOGGER.info("Intantiating")
        self.display = display
        
    def update(self, calendar):
        if calendar.special_day_today:
            self._handle_special_day(calendar)
        else:
            self._handle_regular_day(calendar)

    def _handle_special_day(self, calendar):
        msg = "It's {}!".format(calendar.todays_event)
        LOGGER.info(
            "Updating with calendar {}. Setting message to {}"
            .format(calendar, msg))
        self.display.clear()       
        self.display.show_message(msg)
    
    def _handle_regular_day(self, calendar):
        sleeps = calendar.sleeps_to_next_event
        unit = 'sleeps' if sleeps > 1 else 'sleep'
        msg = "{} in {} {}".format(
            calendar.next_event, sleeps, unit)
        LOGGER.info(
            "Updating with calendar {}. Setting message to {}"
            .format(calendar, msg))
        self.display.clear()       
        self.display.show_message(msg)
        LOGGER.info("Setting message to {}".format(sleeps))
        self.display.show_message(str(sleeps))
