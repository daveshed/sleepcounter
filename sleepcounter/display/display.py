"""
Led matrix interface implemenation which extends the abstract base class and
makes calls to the driver simpler.
"""
from time import sleep
from PIL import ImageFont

from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219

from sleepcounter.display.interface import LedMatrixInterface
from sleepcounter.fonts.library import AVAILABLE_FONTS

FONT_PATH = AVAILABLE_FONTS['Vera.ttf']
FONT_SIZE = 9
FONT = ImageFont.truetype(font=FONT_PATH, size=FONT_SIZE)
SCROLL_RATE = 40 # pixels per second
VERTICAL_OFFSET = 0


class LedMatrix(LedMatrixInterface):
    """Led matrix implementation - an interface to the luma core library"""
    def __init__(self, display: max7219):
        """Creates the interface from a MAX7219 display instance"""
        self.display = display
        self.virtual = viewport(display, width=200, height=100)

    def show_message(self, message, scroll=False):
        text = message.upper()
        text_length, _ = FONT.getsize(text)
        # automatically scroll if the message is too long
        if text_length > self.display.width:
            scroll = True
        if not scroll:
            self._show_text(text)
        else:
            for offset in range(text_length + self.display.width):
                self._show_text(text, self.display.width - offset)
                sleep(1 / SCROLL_RATE)

    def clear(self):
        self.display.clear()

    def _show_text(self, text, offset=0):
        with canvas(self.virtual) as draw:
            draw.text(
                (offset, VERTICAL_OFFSET),
                text,
                font=FONT,
                fill="white",
            )
