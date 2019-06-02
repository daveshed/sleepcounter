from logging import getLogger
from unittest.mock import Mock

_LOGGER = getLogger("mock matrix")


class Matrix:

    _width = 32
    _height = 8
    _mode = "1"

    def __init__(self):
        _LOGGER.info("Created mock led matrix device %r" % self)
        self.display = Mock()

    @property
    def width(self):
        return Matrix._width

    @property
    def height(self):
        return Matrix._height
    
    @property
    def mode(self):
        return Matrix._mode

    def clear(self):
        _LOGGER.info("Clearing device %r" % self)
