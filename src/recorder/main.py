import time
import sys
import argparse
from datetime import datetime
from pathlib import Path
from recorder.system.runner import ServiceRunner
from recorder.BNO055.imu_service import IMUService
from recorder.camera.camera_service import CameraService


def parse_args(args):
    parser = argparse.ArgumentParser(description="Starts measurement recording")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Flag if continuous recording shall be activated.",
    )
    parser.add_argument(
        "--max_recordings",
        type=int,
        help="Maximum number of recordings that shall be captured.",
        default=10,
    )
    parsed_args = parser.parse_args(args)
    return parsed_args


def record_single_measurement():
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


if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    print(parsed_args.max_recordings)
    print(parsed_args.loop)
    for i in range(parsed_args.max_recordings):
        print(f"===== Starting recording {i} =====")
        record_single_measurement()
        print(f"===== Finished recording {i} =====")
        if not parsed_args.loop:
            break
