"""Implements a python process class"""

from abc import ABC, abstractmethod
from multiprocessing import Process, Event
from pathlib import Path


class PythonProcess(ABC):
    def __init__(self, start_time: float, logging_directory: str | Path):
        self.proc: Process | None = None
        self.stop_event = Event()
        self.start_time = start_time
        self.logging_directory = Path(logging_directory)

    @staticmethod
    @abstractmethod
    def run(stop_event, start_time, logging_directory):
        """Business logic to be implemented by the child class."""
        raise NotImplementedError

    def start(self):
        if self.proc is not None:
            return

        self.proc = Process(
            target=self.run,
            args=(self.stop_event, self.start_time, self.logging_directory),
        )
        self.proc.start()

    def stop(self) -> None | int:
        if self.proc is None:
            return None

        # notify process to stop
        self.stop_event.set()
        self.proc.join(timeout=15)

        # check if process is terminated
        if self.proc.exitcode is None:
            self.proc.kill()
            self.proc.join(timeout=1)

        ret = self.proc.exitcode

        self.proc.close()
        self.proc = None

        return ret
