import time


class RateKeeper:
    """Implements a rate keeper that can be used inside a loop to execute code periodically with a given rate."""

    def __init__(self, rate: float):
        self._interval = 1.0 / rate
        self._last_monitor_time = time.monotonic()

    def wait(self):
        current_time = time.monotonic()
        elapsed_time = current_time - self._last_monitor_time
        waiting_time = max(0, self._interval - elapsed_time)
        time.sleep(waiting_time)
        self._last_monitor_time = time.monotonic()
