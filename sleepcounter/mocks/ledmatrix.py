"""
Mocks out led device hardware
"""
from logging import getLogger
from unittest.mock import Mock

_LOGGER = getLogger("mock matrix")


class Matrix:
    """
    A mock for an led matrix device
    """
    _width = 32
    _height = 8
    _mode = "1"

    def __init__(self):
        _LOGGER.info("Created mock led matrix device %r", self)
        self.display = Mock()

    @property
    def width(self):
        """
        Width of the display in pixels
        """
        return Matrix._width

    @property
    def height(self):
        """
        Height of the display in pixels
        """
        return Matrix._height

    @property
    def mode(self):
        """
        Returns mode which is needed for image drawing reasons
        """
        return Matrix._mode

    def clear(self):
        """
        Clear the display
        """
        _LOGGER.info("Clearing device %r", self)
