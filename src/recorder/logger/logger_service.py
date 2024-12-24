import threading
from pathlib import Path
from recorder.mw.service import Service
from recorder.mw.rate_keeper import RateKeeper
from recorder.logger.imu_logger import ImuLogger


class LoggerService(Service):

    def __init__(self, start_time: float, logging_directory: str | Path):
        self._loggers = [ImuLogger(start_time, logging_directory)]
        self._logger_threads = [None for _ in self._loggers]

    def run(self, stop_event):
        # start logger threads
        for i in range(len(self._logger_threads)):
            if self._logger_threads[i] is None:
                self._logger_threads[i] = threading.Thread(target=self._loggers[i].log)
                self._logger_threads[i].start()

        rk = RateKeeper(10)
        while not stop_event.is_set():
            rk.wait()

        # shutdown logger threads
        for i in range(len(self._logger_threads)):
            if self._logger_threads[i] and self._logger_threads[i].is_alive():
                self._loggers[i].stop()
                self._logger_threads[i].join()
