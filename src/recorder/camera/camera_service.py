import time
from pathlib import Path
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from recorder.system.process import PythonProcess


class CameraServiceImplementation:
    def __init__(self, rec_start_time: float, logging_directory: str | Path):
        self._picam = Picamera2()
        video_config = self._picam.create_video_configuration(
            controls={"FrameDurationLimits": (40000, 40000)}
        )
        self._picam.configure(video_config)
        self._rec_start_time = rec_start_time
        self._logging_directory = Path(logging_directory)
        self._time_offset = None
        self._picam.pre_callback = self.get_time_offset
        self._encoder = H264Encoder()

    def get_time_offset(self, request):
        if self._time_offset is None:
            self._time_offset = time.monotonic() - self._rec_start_time
            self._time_offset *= 1000

    def start(self):
        self._picam.start_recording(
            self._encoder,
            str(self._logging_directory / "video.h264"),
            pts=str(self._logging_directory / "frame_timestamps.txt"),
            quality=Quality.HIGH,
        )

    def stop(self):
        self._picam.stop_recording()
        self.postprocess()

    def postprocess(self):
        with open(self._logging_directory / "frame_timestamps.txt", "r") as f:
            frame_timestamps = [float(line.strip()) for line in f]

        with open(self._logging_directory / "frame_timestamps.txt", "w") as f:
            for timestamp in frame_timestamps:
                f.write(f"{timestamp+self._time_offset}\n")


class CameraService(PythonProcess):
    def __init__(self, start_time: float, logging_directory: str | Path):
        super().__init__(start_time, logging_directory)

    @staticmethod
    def run(stop_event, start_time, logging_directory):
        service_implementation = CameraServiceImplementation(
            rec_start_time=start_time, logging_directory=logging_directory
        )
        service_implementation.start()
        while not stop_event.is_set():
            time.sleep(0.04)
        service_implementation.stop()