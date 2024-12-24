import time
import struct
from pathlib import Path
from ipc_pyx import PubSocket
from recorder.mw.service import Service
from recorder.mw.rate_keeper import RateKeeper
from recorder.BNO055.lib.bno055 import BNO055


class IMUService(Service):
    def __init__(self, start_time: float, logging_directory: str | Path):
        self._start_time = start_time
        self._logging_directory = logging_directory
        self._sensor = BNO055()
        self._pub_socket = PubSocket(b"/imu")
        self._msg_fmt = "fffffff"

    def run(self, stop_event):
        rate_keeper = RateKeeper(100)
        while not stop_event.is_set():
            self.publish()
            rate_keeper.wait()

    def read(self):
        timestamp = time.monotonic()
        acc_vec = self._sensor.read_acc_data()
        gyr_vec = self._sensor.read_gyr_data()
        msg_data = (timestamp, *acc_vec, *gyr_vec)
        return msg_data

    def publish(self):
        msg_data = self.read()
        packed_msg_data = struct.pack(self._msg_fmt, *msg_data)
        self._pub_socket.send(packed_msg_data)
