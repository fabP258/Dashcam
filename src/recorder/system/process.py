"""Implements a python process class"""

from abc import ABC, abstractmethod
from multiprocessing import Process


class PythonProcess(ABC):
    def __init__(self):
        self.proc: Process | None = None

    @abstractmethod
    def run(self):
        raise NotImplementedError

    def start(self):
        if self.proc is not None:
            return

        self.proc = Process(target=self.run)
        self.proc.start()

    def stop(self) -> None | int:
        if self.proc is None:
            return None

        # check if process is terminated
        if self.proc.exitcode is None:
            self.proc.kill()
            self.proc.join(timeout=1)

        ret = self.proc.exitcode

        self.proc.close()
        self.proc = None

        return ret
