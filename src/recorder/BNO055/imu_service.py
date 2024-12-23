import time
import struct
from pathlib import Path
from typing import List
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
        data = []
        rate_keeper = RateKeeper(100)
        while not stop_event.is_set():
            data.append(self.read_sensor_data())
            rate_keeper.wait()
        IMUService.write_data(data, self._start_time, self._logging_directory)

    @staticmethod
    def write_data(data: List[tuple], start_time: float, logging_directory: Path):

        def list_to_str(lst: List[float]):
            return ",".join(str(val) for val in lst)

        with open(logging_directory / "imu_data.txt", "w") as f:
            f.write("timestamp,ax,ay,az,wx,wy,wz\n")
            for t, acc_vec, gyr_vec in data:
                f.write(
                    f"{t-start_time},{list_to_str(acc_vec)},{list_to_str(gyr_vec)}\n"
                )

    def read_sensor_data(self):
        timestamp = time.monotonic()
        acc_vec = self._sensor.read_acc_data()
        gyr_vec = self._sensor.read_gyr_data()

        # publish message via IPC
        msg_data = (timestamp, *acc_vec, *gyr_vec)
        packed_msg_data = struct.pack(self._msg_fmt, *msg_data)
        self._pub_socket.send(packed_msg_data)

        return timestamp, acc_vec, gyr_vec
