import struct
from pathlib import Path
from recorder.mw.rate_keeper import RateKeeper
from recorder.logger.logger_base import LoggerBase
from ipc_pyx import SubSocket


class ImuLogger(LoggerBase):

    def __init__(self, start_time: float, logging_directory: str | Path):
        super().__init__(logging_directory)
        self._start_time = start_time
        self._sub_socket = SubSocket(b"/imu")
        self._msg_fmt = "fffffff"
        self._msg_header = [
            "timestamp",
            "ax",
            "ay",
            "az",
            "wx",
            "wy",
            "wz",
        ]

    def log(self):
        rate_keeper = RateKeeper(150)
        with open(self._logging_directory / "imu_data.txt", "w") as f:
            f.write(ImuLogger.list_to_cs_str(self._msg_header) + "\n")
            while not self._stop_flag.is_set():
                byte_data = self._sub_socket.receive()
                if byte_data is not None:
                    unpacked_data = struct.unpack(self._msg_fmt, byte_data)
                    unpacked_data = (
                        unpacked_data[0] - self._start_time,
                    ) + unpacked_data[1:]
                    f.write(ImuLogger.list_to_cs_str(unpacked_data) + "\n")
                rate_keeper.wait()

    @staticmethod
    def list_to_cs_str(lst: list):
        return ",".join(str(val) for val in lst)
