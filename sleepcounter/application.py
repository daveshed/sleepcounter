"""
Sleepcounter application
"""
from logging import getLogger

_LOGGER = getLogger("application")


class Application:
    """
    The sleepcounter application class that manages the starting and stopping
    of all its date display widgets.

    keyword arguments:
    widgets -- a list of all widgets to be run
    """
    def __init__(self, widgets: list):
        self._widgets = widgets

    def start(self):
        """Start all the widgets"""
        _LOGGER.info("Starting widgets...")
        for widget in self._widgets:
            _LOGGER.info("Starting widget %s", widget)
            widget.start()

    def stop(self):
        """Stop all the widgets"""
        _LOGGER.info("Stopping widgets...")
        for widget in self._widgets:
            _LOGGER.info("Stopping widget %s", widget)
            widget.stop()
