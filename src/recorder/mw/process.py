"""Implements a python process class"""

from multiprocessing import Process, Event
from recorder.system.service import Service


class PythonProcess:
    def __init__(
        self,
        service: Service,
    ):
        self.proc: Process | None = None
        self.stop_event = Event()
        self.service = service

    @staticmethod
    def run(stop_event, service: Service):
        service.run(stop_event)

    def start(self):
        if self.proc is not None:
            return

        self.proc = Process(
            target=self.run,
            args=(
                self.stop_event,
                self.service,
            ),
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
