"""
Controller class module
"""
from sleepcounter.time.calendar import Calendar


class Controller:
    """
    Holds references to different date display widgets and notifies them when
    called to do so.

    Keyword arguments:
    calendar -- a Calendar object
    """

    def __init__(self, calendar: Calendar):
        self._widgets = []
        self.calendar = calendar

    def update_widgets(self):
        """Update all registerd widgets with latest calendar informations"""
        for widget in self._widgets:
            widget.update(self.calendar)

    def register_widget(self, widget):
        """Register another widget to be updated"""
        self._widgets.append(widget)

    def deregister_widget(self, widget):
        """Deregister a widget to stop it being updated"""
        self._widgets.remove(widget)
