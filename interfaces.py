from abc import ABCMeta, abstractmethod


class EventSender(metaclass=ABCMeta):

    @abstractmethod
    def click(self, x, y):
        pass


class ScreenFetcher(metaclass=ABCMeta):

    @abstractmethod
    def capture(self, path):
        pass
