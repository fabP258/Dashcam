import time

from recorder.BNO055.imu_service import IMUService
from recorder.camera.camera_service import CameraService
from recorder.system.runner import ServiceRunner

if __name__ == "__main__":
    start_time = time.monotonic()
    services = []
    services.append(IMUService(start_time=start_time))
    services.append(CameraService(start_time=start_time))
    runner = ServiceRunner(services)
    runner.start()
