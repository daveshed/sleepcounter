# pylint: disable=invalid-name
"""Defines the interface for all widgets used for displaying time information"""
from abc import ABC, abstractmethod


class BaseWidget(ABC):
    # pylint: disable=too-few-public-methods
    """
    The interface for all widgets to implement. Each widget represents the date
    somehow. They are observers of the Controller class and must implement an
    update method that takes an instance of calendar. The widget can access the
    calendar and act accordingly.
    """
    @abstractmethod
    def update(self, calendar):
        """Method called by the controller class to update widgets"""
