import time
import smbus2
import bno055_registers
import bno055_register_values
from bno055_config import BNO055Config, BNO055AccConfig, BNO055GyrConfig

class BNO055:

    def __init__(self, i2c_address: int = 0x28, i2c_bus_identifier: int = 1, config: BNO055Config = BNO055Config()):
        self._i2c_address = i2c_address
        self._i2c_bus = smbus2.SMBus(i2c_bus_identifier)
        self._op_mode: bno055_register_values.OpMode = None
        self._pwr_mode: bno055_register_values.PwrMode = None
        self.configure_sensor(config)
    
    def set_op_mode(self, op_mode: bno055_register_values.OpMode):
        self.write_byte_data(bno055_registers.OP_MODE_ADDRESS, op_mode.value)
        if op_mode == bno055_register_values.OpMode.CONFIGMODE:
            # Switch from any op mode to cfg mode takes 19 ms (cf. datasheet page 21)
            time.sleep(0.02)
        else:
            # Switch from cfg mode to any op mode takes 7 ms
            time.sleep(0.01)
        self._op_mode = op_mode

    def set_pwr_mode(self, pwr_mode: bno055_register_values.PwrMode):
        self.write_byte_data(bno055_registers.PWR_MODE_ADDRESS, pwr_mode.value)
        self._pwr_mode = pwr_mode

    def write_byte_data(self, register, value):
        self._i2c_bus.write_byte_data(self._i2c_address, register, value)

    # TODO: DEPRECATED
    def switch_register_page(self, page: hex):
        if not (page == 0x00 or page == 0x01):
            raise ValueError(f"Page value {page} is not allowed.")
        self.write_byte_data(bno055_registers.PAGE_SELECT_ADDRESS, page)

    def switch_register_page(self, page: hex):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not (page == 0x00 or page == 0x01):
                    raise ValueError(f"Page value {page} is not allowed.")
                self.write_byte_data(bno055_registers.PAGE_SELECT_ADDRESS, page)
                try:
                    result = func(*args, **kwargs)
                finally:
                    self.write_byte_data(bno055_registers.PAGE_SELECT_ADDRESS, 0x00)
                return result
            return wrapper
        return decorator

    def configure_sensor(self, config: BNO055Config):
        # TODO: Validate config (check if str are in dict keys)
        self.set_pwr_mode(config.power_mode)
        # TODO: Handle low power mode? --> acc can't be configured
        self.set_op_mode(bno055_register_values.OpMode.CONFIGMODE)
        self._configure_acc(config.accelerometer)
        self._configure_gyr(config.gyroscope)
        self.set_op_mode(config.operation_mode)

    @switch_register_page(0x01)
    def _configure_acc(self, acc_config: BNO055AccConfig):
        if not (self._op_mode == bno055_register_values.OpMode.CONFIGMODE):
            raise Warning("Could not configure accelerometer. Sensor is not in config mode.")
        self.write_byte_data(bno055_registers.ACC_CONFIG, acc_config.get_register_value())

    @switch_register_page(0x01)
    def _configure_gyr(self, gyr_config: BNO055GyrConfig):
        if not (self._op_mode == bno055_register_values.OpMode.CONFIGMODE):
            raise Warning("Could not configure accelerometer. Sensor is not in config mode.")
        gyr_config_0 = self._i2c_bus.read_byte_data(self._i2c_address, bno055_registers.GYRO_CONFIG_0)
        reserved_mask0 = 0b11000000
        gyr_config_0 &= reserved_mask0
        new_gyr_config_0 = gyr_config_0 | gyr_config.get_register_value_0()
        self.write_byte_data(bno055_registers.GYRO_CONFIG_0, new_gyr_config_0)
        gyr_config_1 = self._i2c_bus.read_byte_data(self._i2c_address, bno055_registers.GYRO_CONFIG_1)
        reserved_mask1 = 0b11111000
        gyr_config_1 &= reserved_mask1
        new_gyr_config_1 = gyr_config_0 | gyr_config.get_register_value_1()
        self.write_byte_data(bno055_registers.GYRO_CONFIG_1, new_gyr_config_1)

    def read_16bit_register(self, register_low):
        low_byte = self._i2c_bus.read_byte_data(self._i2c_address, register_low)
        high_byte = self._i2c_bus.read_byte_data(self._i2c_address, register_low + 1)
        value = (high_byte << 8) | low_byte

        # convert value to signed int (16 Bit)
        if value > 32767:
            value -= 65536
        return value
    
    def read_acc_data(self):
        # TODO: check if op_mode supports acc readings
        acc_x = self.read_16bit_register(bno055_registers.ACCEL_DATA_X_LSB_ADDRESS)
        acc_y = self.read_16bit_register(bno055_registers.ACCEL_DATA_Y_LSB_ADDRESS)
        acc_z = self.read_16bit_register(bno055_registers.ACCEL_DATA_Z_LSB_ADDRESS)

        # TODO: convert from signed int to float

    def read_gyr_data(self):
        # TODO: check if op_mode supports gyro readings
        rate_x = self.read_16bit_register(bno055_registers.GYRO_DATA_X_LSB_ADDRESS)
        rate_y = self.read_16bit_register(bno055_registers.GYRO_DATA_Y_LSB_ADDRESS)
        rate_z = self.read_16bit_register(bno055_registers.GYRO_DATA_Z_LSB_ADDRESS)

        # TODO: convert from signed int to float


