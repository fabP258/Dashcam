import threading
from abc import ABC, abstractmethod
from pathlib import Path


class LoggerBase(ABC):

    def __init__(self, logging_directory: str | Path):
        self._logging_directory = Path(logging_directory)
        self._stop_flag = threading.Event()

    @abstractmethod
    def log(self):
        raise NotImplementedError

    def stop(self):
        self._stop_flag.set()
