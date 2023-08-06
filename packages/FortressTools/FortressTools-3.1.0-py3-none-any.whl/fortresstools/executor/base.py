from abc import ABC, abstractmethod


class BaseExecutor(ABC):
    def __init__(self):
        pass


    @abstractmethod
    def run(self, cmd, *cmds):
        pass
