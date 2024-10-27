import time
import bno055
import bno055_config

config = bno055_config.BNO055Config()
sensor = bno055.BNO055(config=config)
calib_status = sensor.calibration_status()

for idx in range(1000):
    (x, y, z) = sensor.read_gyr_data()
    print(f"{x:<10} {y:<10} {z:<10}")
    time.sleep(0.1)
