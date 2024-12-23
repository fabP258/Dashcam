from abc import ABC, abstractmethod


class Service(ABC):

    @abstractmethod
    def run(self, stop_event):
        raise NotImplementedError
