import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from recorder.system.process import PythonProcess


class CameraService(PythonProcess):
    def __init__(self):
        super().__init__()

    @staticmethod
    def run(stop_event):
        picam = Picamera2()
        video_config = picam.create_video_configuration(
            controls={"FrameDurationLimits": (40000, 40000)}
        )
        picam.configure(video_config)
        encoder = H264Encoder()
        picam.start_recording(
            encoder, "test.h264", pts="frame_timestamps.txt", quality=Quality.HIGH
        )
        while not stop_event.is_set():
            time.sleep(0.04)
        picam.stop_recording()
