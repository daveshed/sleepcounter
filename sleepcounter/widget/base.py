# pylint: disable=invalid-name
"""Defines the interface for all widgets used for displaying time information"""
from abc import ABC, abstractmethod
from logging import getLogger
from threading import Event, Thread
from time import sleep

_LOGGER = getLogger("widget")


class BaseWidget(ABC, Thread):
    # pylint: disable=too-few-public-methods
    """
    The interface for all widgets to implement. Each widget represents the date
    somehow. They are observers of the Controller class and must implement an
    update method that takes an instance of calendar. The widget can access the
    calendar and act accordingly.
    """
    daemon = True
    mins_between_updates = 120

    def __init__(self, calendar, label=None):
        self._label = label
        self._calendar = calendar
        self._running = Event()
        super().__init__(target=self._refresh, daemon=BaseWidget.daemon)
        _LOGGER.info(
            "Instantiated %s daemon widget %r",
            ("" if BaseWidget.daemon else "non"),
            self)

    @property
    def label(self):
        """Retreive the label of the widget"""
        return self._label

    @property
    def running(self):
        """Retrieve the status of the widget's thread of activity"""
        return self._running.is_set()

    def start(self):
        """Start the widget's thread of activity"""
        if not self.running:
            _LOGGER.info("Starting widget %r...", self)
            self._running.set()
            super().start()
            _LOGGER.info("Widget %r has started", self)
        else:
            _LOGGER.info("Widget %r already running", self)

    def stop(self):
        """Stop the widget's thread of activity"""
        if self.running:
            _LOGGER.info("Stopping widget %r...", self)
            self._running.clear()
        else:
            _LOGGER.info("Widget %r is not running", self)

    @abstractmethod
    def update(self):
        """Method called by the controller class to update widgets"""

    def __repr__(self):
        return "%r: label=%s" % (super().__repr__(), self.label)

    def _refresh(self):
        while self.running:
            self.update()
            sleep(60 * BaseWidget.mins_between_updates)
        _LOGGER.info("Widget %r has stopped", self)
