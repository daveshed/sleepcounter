import logging
import datetime

logger = logging.getLogger("calendar")

class Calendar:
    """
    Interface to the date library that allows you to lookup the next event and 
    find out what is happening today.
    """
    def __init__(self, date_library):
        logger.info("Instantiated with date_library {}".format(date_library))
        self.date_library = date_library

    def time_to_event(self, ev):
        date = self.date_library.get_date(ev)
        delta = date - datetime.datetime.today()
        logger.info("Time to event {} is {}".format(ev, delta))
        return delta

    def seconds_to_event(self, ev):
        ret_val = self.time_to_event(ev).total_seconds()
        logger.info("{} seconds to event {}".format(ret_val, ev))
        return ret_val

    def days_to_event(self, ev):
        ret_val = self.time_to_event(ev).days
        logger.info("{} days to event {}".format(ret_val, ev))
        return ret_val

    @property
    def next_event(self):
        deltas = {ev: self.days_to_event(ev) for ev in self.date_library.events}
        next_event = min(deltas, key=deltas.get)
        logger.info("Next event is {}".format(next_event))
        return next_event

    @property
    def special_day_today(self):
        special = self.todays_event is not None
        logger.info("Today is special {}".format(special))
        return special

    @property
    def todays_event(self):
        event = None
        if self.days_to_next_event == 0:
            event = self.next_event
        logger.info("Todays event is {}".format(event))
        return event

    @property
    def seconds_to_next_event(self):
        ret_val = self.seconds_to_event(self.next_event)
        logger.info("{} seconds to next event".format(ret_val))
        return ret_val

    @property
    def days_to_next_event(self):
        ret_val = self.days_to_event(self.next_event)
        logger.info("{} days to next event".format(ret_val))
        return ret_val

    @property
    def daytime(self):
        pass
    
    @property
    def nighttime(self):
        return not self.daytime