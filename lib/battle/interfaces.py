from abc import ABCMeta, abstractmethod
from ..base import logger, config


class Task(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, capture):
        pass

    def execute(self, capture):
        capture_name = capture.replace(config.temp_folder_path, "")
        logger.log("{} executed at {}".format(type(self).__name__, capture_name))
        self.on_execute(capture)

    @abstractmethod
    def on_execute(self, capture):
        pass
