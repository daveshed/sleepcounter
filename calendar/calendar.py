import datetime

from displayitem import DisplayItem

class Foo:
    pass

class DateLibrary:

    def __init__(self, events={}):
        self._events = events

    @property
    def events(self):
        return self._events

    def get_date(self, ev):
        return self._events[ev]
        
    def remove_event(self, ev):
        try:
            del self._events[ev]
        except KeyError:
            raise Warning("{} not listed".format(ev))

    def add_event(self, ev, date):
        if ev in self._events.keys():
            raise Warning("{} already exists".format(ev))
        else:
            self._events[ev] = date

    def clear_events(self):
        self._events = {}


class Calendar:

    def __init__(self, date_library):
        self.date_library = date_library

    def days_to_event(self, ev):
        date = self.date_library.get_date(ev)
        delta = date - datetime.datetime.today()
        return delta.days

    @property
    def next_event(self):
        deltas = {ev: self.days_to_event(ev) for ev in self.date_library.events}
        return min(deltas, key=deltas.get)

    @property
    def todays_event(self):
        if self.days_to_next_event == 0:
            return self.next_event
        else:
            return None

    @property
    def days_to_next_event(self):
        return self.days_to_event(self.next_event)

    @property
    def daytime(self):
        pass
    
    @property
    def nighttime(self):
        return not self.daytime