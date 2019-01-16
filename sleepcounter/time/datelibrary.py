"""
Module that holds the DateLibrary class only
"""

class DateLibrary:
    """
    A library class that contains date objects. The library can be interrogated
    for the next event and events can be added and removed later.

    Keyword arguments:
    events -- a dictionary of event objects
    """
    def __init__(self, events=None):
        if not events:
            self._events = {}
        else:
            self._events = events

    @property
    def events(self):
        """get event dictionary"""
        return self._events

    def get_date(self, event: str):
        """get the date that a given event happens"""
        return self._events[event]

    def get_event(self, search_date):
        """get the event corresponding to a given search date"""
        event = None
        for name, date in self.events.items():
            if date == search_date:
                event = name
                return event
        return event

    def remove_event(self, event):
        """remove an event from the library"""
        try:
            del self._events[event]
        except KeyError:
            raise Warning("{} not listed".format(event))

    def add_event(self, event, date):
        """add an event to the library"""
        if event in self._events.keys():
            raise Warning("{} already exists".format(event))
        else:
            self._events[event] = date

    def clear_events(self):
        """clear all events from the library"""
        self._events = {}
