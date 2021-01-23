from abc import ABCMeta, abstractmethod


class ScreenFetcher(metaclass=ABCMeta):

    @abstractmethod
    def fetch(self, path):
        pass



