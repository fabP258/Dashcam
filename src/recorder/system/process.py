"""Implements a python process class"""

from abc import ABC, abstractmethod
from multiprocessing import Process, Event


class PythonProcess(ABC):
    def __init__(self):
        self.proc: Process | None = None
        self.stop_event = Event()

    @staticmethod
    @abstractmethod
    def run(stop_event):
        """Business logic to be implemented by the child class."""
        raise NotImplementedError

    def start(self):
        if self.proc is not None:
            return

        self.proc = Process(target=self.run, args=(self.stop_event,))
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
