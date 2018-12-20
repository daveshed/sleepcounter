from linearstage.stage import OutOfRangeError


class MockStage:
    MAX_POS = 100
    MIN_POS = 0

    def __init__(self):
        self.home()

    def home(self):
        self._position = __class__.MIN_POS

    def end(self):
        self._position = self.max

    @property
    def max(self):
        return __class__.MAX_POS

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, request):
        too_large = request > __class__.MAX_POS
        too_small = request < __class__.MIN_POS
        if too_large or too_small:
            raise OutOfRangeError("Cannot go to position {}"
                .format(request))
        self._position = request
