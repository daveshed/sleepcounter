class DateLibrary:
    """
    A library class that contains date objects. The library can be interrogated
    for the next event and events can be added and removed later.
    
    Keyword arguments:
    events -- a dictionary of event objects    
    """
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