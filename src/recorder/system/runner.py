import time
from typing import List

from recorder.system.process import PythonProcess


class ServiceRunner:
    def __init__(self, services: List[PythonProcess]):
        self._services = services

    def start(self):
        for service in self._services:
            service.start()
        self.monitor()

    def stop(self):
        for service in reversed(self._services):
            service.stop()

    def monitor(self):
        time.sleep(60)
        self.stop()
