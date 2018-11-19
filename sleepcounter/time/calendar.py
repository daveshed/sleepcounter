import datetime


class Calendar:
    """
    Interface to the date library that allows you to lookup the next event and 
    find out what is happening today.
    """
    def __init__(self, date_library):
        self.date_library = date_library

    def time_to_event(self, ev):
        date = self.date_library.get_date(ev)
        delta = date - datetime.datetime.today()
        return delta

    def seconds_to_event(self, ev):
        return self.time_to_event(ev).total_seconds()

    def days_to_event(self, ev):
        return self.time_to_event(ev).days

    @property
    def next_event(self):
        deltas = {ev: self.days_to_event(ev) for ev in self.date_library.events}
        return min(deltas, key=deltas.get)

    @property
    def special_day_today(self):
        return self.todays_event is not None

    @property
    def todays_event(self):
        if self.days_to_next_event == 0:
            return self.next_event
        else:
            return None

    @property
    def seconds_to_next_event(self):
        return self.seconds_to_event(self.next_event)

    @property
    def days_to_next_event(self):
        return self.days_to_event(self.next_event)

    @property
    def daytime(self):
        pass
    
    @property
    def nighttime(self):
        return not self.daytime