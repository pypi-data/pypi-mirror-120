from abc import ABC, abstractmethod


class BaseCommand(ABC):
    def __init__(self, executor, **kwargs):
        self._executor = executor
        for key, value in kwargs.items():
            setattr(self, key, value)
        if "options" not in self.__dict__:
            self.options = ""

    @abstractmethod
    def execute(self):
        pass
