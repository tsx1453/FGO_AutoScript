from abc import ABCMeta, abstractmethod


class EventSender(metaclass=ABCMeta):

    @abstractmethod
    def click(self, x, y):
        pass


class ScreenFetcher(metaclass=ABCMeta):

    @abstractmethod
    def capture(self, path):
        pass


class State(metaclass=ABCMeta):

    @abstractmethod
    def match(self, capture_path):
        pass

    @abstractmethod
    def execute(self):
        pass


class Runner(metaclass=ABCMeta):

    @abstractmethod
    def run(self, capture_path):
        pass
