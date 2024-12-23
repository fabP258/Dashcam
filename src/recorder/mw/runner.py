from typing import List
from recorder.mw.process import PythonProcess
from recorder.mw.service import Service
from recorder.mw.rate_keeper import RateKeeper


class ServiceRunner:
    def __init__(self, services: List[Service]):
        self._services = [PythonProcess(service) for service in services]

    def start(self):
        for service in self._services:
            service.start()
        self.monitor()

    def stop(self):
        for service in reversed(self._services):
            service.stop()

    def monitor(self):
        rate_keeper = RateKeeper(1)
        start_time = rate_keeper.get_last_monitor_time()
        while True:
            rate_keeper.wait()
            elapsed_time = rate_keeper.get_last_monitor_time() - start_time
            print(f"REC: {elapsed_time:.2f} s")
            if elapsed_time >= 60:
                break
        print("Stopping recording ...")
        self.stop()
