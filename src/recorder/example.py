import time
from recorder.BNO055.bno055 import BNO055
from recorder.system.periodic_task import PeriodicTask


def read_and_store_imu(sensor: BNO055):
    timestamp = time.time()
    print(timestamp)
    acc_x, acc_y, acc_z = sensor.read_acc_data()


sensor = BNO055()

task = PeriodicTask(0.01, read_and_store_imu, sensor)
task.start()
time.sleep(5)
task.stop()
