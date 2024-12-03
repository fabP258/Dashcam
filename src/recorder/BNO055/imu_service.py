import time
from pathlib import Path
from typing import List
from recorder.system.process import PythonProcess
from recorder.system.rate_keeper import RateKeeper
from recorder.BNO055.lib.bno055 import BNO055


class IMUService(PythonProcess):
    def __init__(self, start_time: float, logging_directory: str | Path):
        super().__init__(start_time, logging_directory)

    @staticmethod
    def run(stop_event, start_time, logging_directory):
        sensor = BNO055()
        data = []
        rate_keeper = RateKeeper(100)
        while not stop_event.is_set():
            data.append(IMUService.read_sensor_data(sensor))
            rate_keeper.wait()
        IMUService.write_data(data, start_time, logging_directory)

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

    @staticmethod
    def read_sensor_data(sensor: BNO055):
        timestamp = time.monotonic()
        acc_vec = sensor.read_acc_data()
        gyr_vec = sensor.read_gyr_data()
        return timestamp, acc_vec, gyr_vec
