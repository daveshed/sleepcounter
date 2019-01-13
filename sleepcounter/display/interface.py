from abc import ABC, abstractmethod

class LedMatrixInterface(ABC):

    @abstractmethod
    def show_message(self, message, scroll=False):
        pass

    @abstractmethod
    def clear(self):
        pass
