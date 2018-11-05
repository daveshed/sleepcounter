from abc import ABC, abstractmethod


class DisplayItem(ABC):

    @abstractmethod
    def update(self):
        pass

class Slider(DisplayItem):
    pass
