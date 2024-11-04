import time
from datetime import datetime
from pathlib import Path
from recorder.system.runner import ServiceRunner
from recorder.BNO055.imu_service import IMUService
from recorder.camera.camera_service import CameraService


if __name__ == "__main__":
    logging_directory = Path("/home/fabio/data") / datetime.now().strftime(
        "%Y%m%d_%H_%M_%S"
    )
    logging_directory.mkdir(parents=True, exist_ok=True)
    start_time = time.monotonic()
    services = []
    services.append(
        IMUService(start_time=start_time, logging_directory=logging_directory)
    )
    services.append(
        CameraService(start_time=start_time, logging_directory=logging_directory)
    )
    runner = ServiceRunner(services)
    runner.start()
