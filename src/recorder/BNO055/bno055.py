import time
import smbus2
import recorder.BNO055.bno055_registers as bno055_registers
import recorder.BNO055.bno055_register_values as bno055_register_values
import recorder.BNO055.bno055_config as bno055_config
import recorder.BNO055.bno055_status as bno055_status


class BNO055:

    def __init__(
        self,
        i2c_address: int = 0x28,
        i2c_bus_identifier: int = 1,
        config: bno055_config.BNO055Config = bno055_config.BNO055Config(),
    ):
        self._i2c_address = i2c_address
        self._i2c_bus = smbus2.SMBus(i2c_bus_identifier)
        self._op_mode: bno055_register_values.OpMode = None
        self._pwr_mode: bno055_register_values.PwrMode = None
        # Configure the sensor
        self.configure_sensor(config)
        # TODO: check if configuration was successful by reading it and comparing
        self.config: bno055_config.BNO055Config = config
        # Read and print the sensor configuration
        self.print_config()

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

    def read_byte_data(self, register):
        return self._i2c_bus.read_byte_data(self._i2c_address, register)

    def switch_register_page(self, page: hex):
        if not (page == 0x00 or page == 0x01):
            raise ValueError(f"Page value {page} is not allowed.")
        self.write_byte_data(bno055_registers.PAGE_SELECT_ADDRESS, page)

    def configure_sensor(self, config: bno055_config.BNO055Config):
        # TODO: Validate config (check if str are in dict keys)
        self.set_pwr_mode(config.power_mode)
        # TODO: Handle low power mode? --> acc can't be configured
        self.set_op_mode(bno055_register_values.OpMode.CONFIGMODE)
        self._configure_units(config.unit)
        self._configure_acc(config.accelerometer)
        self._configure_gyr(config.gyroscope)
        self.set_op_mode(config.operation_mode)
        # TODO: check if configuration was successful by reading it and comparing

    def _configure_acc(self, acc_config: bno055_config.BNO055AccConfig):
        self.switch_register_page(0x01)
        if not (self._op_mode == bno055_register_values.OpMode.CONFIGMODE):
            raise Warning(
                "Could not configure accelerometer. Sensor is not in config mode."
            )
        self.write_byte_data(
            bno055_registers.ACC_CONFIG, acc_config.get_register_value()
        )
        self.switch_register_page(0x00)

    def _configure_gyr(self, gyr_config: bno055_config.BNO055GyrConfig):
        self.switch_register_page(0x01)
        if not (self._op_mode == bno055_register_values.OpMode.CONFIGMODE):
            raise Warning(
                "Could not configure accelerometer. Sensor is not in config mode."
            )
        gyr_config_0 = self._i2c_bus.read_byte_data(
            self._i2c_address, bno055_registers.GYRO_CONFIG_0
        )
        reserved_mask0 = 0b11000000
        gyr_config_0 &= reserved_mask0
        new_gyr_config_0 = gyr_config_0 | gyr_config.get_register_value_0()
        self.write_byte_data(bno055_registers.GYRO_CONFIG_0, new_gyr_config_0)
        gyr_config_1 = self._i2c_bus.read_byte_data(
            self._i2c_address, bno055_registers.GYRO_CONFIG_1
        )
        reserved_mask1 = 0b11111000
        gyr_config_1 &= reserved_mask1
        new_gyr_config_1 = gyr_config_0 | gyr_config.get_register_value_1()
        self.write_byte_data(bno055_registers.GYRO_CONFIG_1, new_gyr_config_1)
        self.switch_register_page(0x00)

    def _configure_units(self, unit_config: bno055_config.BNO055UnitConfig):
        if not (self._op_mode == bno055_register_values.OpMode.CONFIGMODE):
            raise Warning(
                "Could not configure sensor units. Sensor is not in config mode."
            )
        unit_sel_value = self.read_byte_data(bno055_registers.UNIT_SEL)
        reserved_mask = 0b01101000
        unit_sel_value &= reserved_mask
        new_unit_sel_value = unit_sel_value | unit_config.get_register_value()
        self.write_byte_data(bno055_registers.UNIT_SEL, new_unit_sel_value)

    def print_config(self):
        self.switch_register_page(0x01)
        acc_config = bno055_config.BNO055AccConfig.from_register_value(
            self.read_byte_data(bno055_registers.ACC_CONFIG)
        )
        acc_config.print_config()
        gyr_config = bno055_config.BNO055GyrConfig.from_register_value(
            self.read_byte_data(bno055_registers.GYRO_CONFIG_0),
            self.read_byte_data(bno055_registers.GYRO_CONFIG_1),
        )
        gyr_config.print_config()
        self.switch_register_page(0x00)
        unit_config = bno055_config.BNO055UnitConfig.from_register_value(
            self.read_byte_data(bno055_registers.UNIT_SEL)
        )
        unit_config.print_config()

    def calibration_status(self) -> bno055_status.BNO055CalibrationStatus:
        return bno055_status.BNO055CalibrationStatus.from_register_value(
            self.read_byte_data(bno055_registers.CALIB_STAT_ADDRESS)
        )

    def read_16bit_register(self, register_low, signed: bool = True):
        low_byte = self._i2c_bus.read_byte_data(self._i2c_address, register_low)
        high_byte = self._i2c_bus.read_byte_data(self._i2c_address, register_low + 1)
        value = (high_byte << 8) | low_byte

        if signed:
            # convert value to signed int (16 Bit)
            if value > 32767:
                value -= 65536
        return value

    def read_acc_data(self) -> tuple:
        acc_data = (None, None, None)
        if self._op_mode == bno055_register_values.OpMode.CONFIGMODE:
            return acc_data
        if self._op_mode == bno055_register_values.OpMode.MAGONLY:
            return acc_data
        if self._op_mode == bno055_register_values.OpMode.GYROONLY:
            return acc_data
        if self._op_mode == bno055_register_values.OpMode.MAGGYRO:
            return acc_data
        if self._op_mode == bno055_register_values.OpMode.AMG:
            return acc_data
        acc_x = self.read_16bit_register(bno055_registers.ACCEL_DATA_X_LSB_ADDRESS)
        acc_y = self.read_16bit_register(bno055_registers.ACCEL_DATA_Y_LSB_ADDRESS)
        acc_z = self.read_16bit_register(bno055_registers.ACCEL_DATA_Z_LSB_ADDRESS)

        sensitivity = 1  # 1 mg = 1 LSB
        if self.config.unit.acc == "metre_per_square_second":
            sensitivity = 0.01  # 1 m / s^2 = 100 LSB

        acc_x *= sensitivity
        acc_y *= sensitivity
        acc_z *= sensitivity

        return (acc_x, acc_y, acc_z)

    def read_gyr_data(self):
        gyr_data = (None, None, None)
        if self._op_mode == bno055_register_values.OpMode.CONFIGMODE:
            return gyr_data
        if self._op_mode == bno055_register_values.OpMode.ACCONLY:
            return gyr_data
        if self._op_mode == bno055_register_values.OpMode.MAGONLY:
            return gyr_data
        if self._op_mode == bno055_register_values.OpMode.ACCMAG:
            return gyr_data
        if self._op_mode == bno055_register_values.OpMode.AMG:
            return gyr_data
        rate_x = self.read_16bit_register(bno055_registers.GYRO_DATA_X_LSB_ADDRESS)
        rate_y = self.read_16bit_register(bno055_registers.GYRO_DATA_Y_LSB_ADDRESS)
        rate_z = self.read_16bit_register(bno055_registers.GYRO_DATA_Z_LSB_ADDRESS)

        sensitivity = 1.0 / 900.0  # 1 rps = 900 LSB
        if self.config.unit.gyr == "degree_per_second":
            sensitivity = 1.0 / 16.0  # 1dps = 16 LSB

        rate_x *= sensitivity
        rate_y *= sensitivity
        rate_z *= sensitivity

        return (rate_x, rate_y, rate_z)