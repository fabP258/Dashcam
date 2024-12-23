import time
from pathlib import Path
from libcamera import controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from recorder.mw.service import Service


class CameraService(Service):
    def __init__(self, cam_idx: int, start_time: float, logging_directory: str | Path):
        self._cam_idx = cam_idx
        self._start_time = start_time
        self._logging_directory = Path(logging_directory)

    def setup(self):
        self._picam = Picamera2(self._cam_idx)
        self._video_fn = None
        self._timestamp_fn = None
        for cam_info in self._picam.global_camera_info():
            if cam_info["Num"] == self._cam_idx:
                self._video_fn = f"{cam_info['Model']}.h264"
                self._timestamp_fn = f"{cam_info['Model']}_timestamps.txt"
        if self._video_fn is None:
            return
        video_config = self._picam.create_video_configuration(
            main={"size": (1920, 1080), "format": "YUV420"},
            buffer_count=12,
            controls={
                "FrameDurationLimits": (40000, 40000),
                # "ExposureTime": 10000,  # set this lower for calibration
                "AeExposureMode": controls.AeExposureModeEnum.Short,
                "AfMode": controls.AfModeEnum.Manual,
            },
        )
        self._picam.configure(video_config)
        self._time_offset = None
        self._picam.pre_callback = self.get_time_offset
        self._encoder = H264Encoder()

    def get_time_offset(self, request):
        if self._time_offset is None:
            self._time_offset = time.monotonic() - self._start_time
            self._time_offset *= 1000

    def start(self):
        if (self._video_fn is None) or (self._timestamp_fn is None):
            return
        self._picam.start_recording(
            self._encoder,
            str(self._logging_directory / self._video_fn),
            pts=str(self._logging_directory / self._timestamp_fn),
            quality=Quality.HIGH,
        )

    def stop(self):
        self._picam.stop_recording()
        self.postprocess()

    def postprocess(self):
        with open(self._logging_directory / self._timestamp_fn, "r") as f:
            frame_timestamps = [float(line.strip()) for line in f]

        with open(self._logging_directory / self._timestamp_fn, "w") as f:
            for timestamp in frame_timestamps:
                f.write(f"{timestamp+self._time_offset}\n")

    def run(self, stop_event):
        self.setup()
        self.start()
        while not stop_event.is_set():
            time.sleep(0.04)
        self.stop()
