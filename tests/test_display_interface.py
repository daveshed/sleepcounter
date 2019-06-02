import logging
import time

from sleepcounter.display.display import LedMatrix
from sleepcounter.mocks.ledmatrix import Matrix

def test_basic():
    mock_matrix = Matrix()
    foo = LedMatrix(mock_matrix)
    foo.show_message("foobar")
    time.sleep(1)
    foo.show_message("another awesome message!!")
    time.sleep(1)
    foo.show_message("bla")
    foo.clear()
