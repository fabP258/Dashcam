import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from recorder.BNO055.lib.bno055 import BNO055
from recorder.system.periodic_task import PeriodicTask


class Runner:

    def __init__(self):
        self._picam = Picamera2()
        video_config = self._picam.create_video_configuration(
            controls={"FrameDurationLimits": (40000, 40000)}
        )
        self._picam.configure(video_config)
        self._rec_start_time = None
        self._picam.pre_callback = self.rec_start_time
        self._encoder = H264Encoder()
        self._imu = BNO055()
        self._acc_timestamps = []
        self._acc_x = []
        self._acc_y = []
        self._acc_z = []
        self._gyr_x = []
        self._gyr_y = []
        self._gyr_z = []
        self._imu_task = PeriodicTask(0.01, self.read_imu)

    def start(self):
        self._picam.start_recording(
            self._encoder, "test.h264", pts="frame_timestamps.txt", quality=Quality.HIGH
        )
        self._imu_task.start()

    def stop(self):
        self._picam.stop_recording()
        self._imu_task.stop()
        self._acc_timestamps = [t - self._rec_start_time for t in self._acc_timestamps]
        self.write_imu_data()

    def rec_start_time(self, request):
        if self._rec_start_time is None:
            self._rec_start_time = time.perf_counter()

    def read_imu(self):
        timestamp = time.perf_counter()
        acc_x, acc_y, acc_z = self._imu.read_acc_data()
        gyr_x, gyr_y, gyr_z = self._imu.read_gyr_data()
        self._acc_timestamps.append(timestamp)
        self._acc_x.append(acc_x)
        self._acc_y.append(acc_y)
        self._acc_z.append(acc_z)
        self._gyr_x.append(gyr_x)
        self._gyr_y.append(gyr_y)
        self._gyr_z.append(gyr_z)

    def write_imu_data(self):
        with open("imu_data.txt", "w") as f:
            f.write(f"timestamp,ax,ay,az,wx,wy,wz\n")
            for t, ax, ay, az, wx, wy, wz in zip(
                self._acc_timestamps,
                self._acc_x,
                self._acc_y,
                self._acc_z,
                self._gyr_x,
                self._gyr_y,
                self._gyr_z,
            ):
                f.write(f"{t},{ax},{ay},{az},{wx},{wy},{wz}\n")
