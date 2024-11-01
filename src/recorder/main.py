from recorder.system.runner import ServiceRunner
from recorder.BNO055.imu_service import IMUService
from recorder.camera.camera_service import CameraService


if __name__ == "__main__":
    services = []
    services.append(CameraService())
    services.append(IMUService())
    runner = ServiceRunner(services)
    runner.start()
