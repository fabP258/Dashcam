import threading
import time


class PeriodicTask:
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.wakeup_tol = 0.004
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.stop_event = threading.Event()

    def _run(self):
        while not self.stop_event.is_set():
            start_time = time.perf_counter()
            self.function(*self.args, **self.kwargs)
            elapsed_time = time.perf_counter() - start_time
            sleep_time = max(0, self.interval - self.wakeup_tol - elapsed_time)

            # non-blocking sleep
            time.sleep(sleep_time)

            # busy waiting
            while (time.perf_counter() - start_time) <= self.interval:
                time.sleep(0.000001)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()
