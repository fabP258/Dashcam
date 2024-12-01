from abc import ABC, abstractmethod
from recorder.system.message_broker import SharedMemoryMessageBroker


class Service(ABC):

    def __init__(self):
        self._message_broker: None | SharedMemoryMessageBroker = None

    def run(self, stop_event, message_broker: SharedMemoryMessageBroker):
        self._message_broker = message_broker
        self._run(stop_event)

    @abstractmethod
    def _run(self, stop_event):
        raise NotImplementedError
