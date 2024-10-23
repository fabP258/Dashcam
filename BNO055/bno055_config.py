from dataclasses import dataclass, field
import bno055_register_values as reg_vals

@dataclass
class BNO055AccConfig:
    value_range: str = "4G"
    bandwidth: str = "62.5Hz"
    op_mode: str = "Normal"

    def get_register_value(self):
        if self.value_range not in reg_vals.ACC_G_RANGE.keys():
            raise ValueError(f"Accelerometer value range {self.value_range} not supported by sensor.")
        if self.bandwidth not in reg_vals.ACC_BANDWIDTH.keys():
            raise ValueError(f"Accelerometer bandwidth {self.bandwidth} not supported by sensor.")
        if self.op_mode not in reg_vals.ACC_OP_MODE.keys():
            raise ValueError(f"Accelerometer operation mode {self.op_mode} not supported by sensor.")
        return reg_vals.compose_acc_config(reg_vals.ACC_G_RANGE[self.value_range], reg_vals.ACC_BANDWIDTH[self.bandwidth], reg_vals.ACC_OP_MODE[self.op_mode])

    @classmethod
    def from_register_value(cls, register_value: int):
        # TODO: create the object from the int register value and the dict maps
        print(bin(register_value))
        # extract rightmost 8 bit --> necessary? register_value is 8 bit at max
        rightmost_byte = register_value & 0xFF
        # read bits from lsb to msb
        for i in range(8):
            # shift and extract LSB
            lsb = (rightmost_byte >> i) & 1
            print(f"Bit {i}: {lsb}")
            # TODO: map to member variables
        return cls

@dataclass
class BNO055GyrConfig:
    value_range: str = "2000dps"
    bandwidth: str = "32Hz"
    op_mode: str = "Normal"

    # TODO: Config is splitted into two registers, account for this
    def get_register_value_0(self):
        if self.value_range not in reg_vals.GYR_RANGE.keys():
            raise ValueError(f"Gyroscope value range {self.value_range} not supported by sensor.")
        if self.bandwidth not in reg_vals.GYR_BANDWIDTH.keys():
            raise ValueError(f"Gyroscope bandwidth {self.bandwidth} not supported by sensor.")
        # NOTE: Here only 6 Bits are returned since bit7 and bit6 are reserved
        return (reg_vals.GYR_BANDWIDTH[self.bandwidth] << 3) | reg_vals.GYR_RANGE[self.value_range]
    
    def get_register_value_1(self):
        if self.op_mode not in reg_vals.GYR_OP_MODE.keys():
            raise ValueError(f"Gyroscope operation mode {self.op_mode} not supported by sensor.")
        # NOTE: Here only 3 Bits are returned since bit3 to bit7 are reserved
        return reg_vals.GYR_OP_MODE[self.op_mode]
    
    @classmethod
    def from_register_value(cls, register_value0: int, register_value1):
        # TODO: create the object from the int register value and the dict maps
        return cls

@dataclass
class BNO055UnitConfig:
    acc: str = "metre_per_square_second"
    gyr: str = "radian_per_second"
    euler_angles: str = "radian"
    temp: str = "celsius"
    fus_data: str = "Android"

    def get_register_value(self):
        if self.acc not in reg_vals.ACC_UNIT.keys():
            raise ValueError(f"Acceleration unit {self.acc} is undefined.")
        if self.gyr not in reg_vals.GYR_UNIT.keys():
            raise ValueError(f"Angular rate unit {self.gyr} is undefined.")
        if self.euler_angles not in reg_vals.EUL_ANG_UNIT.keys():
            raise ValueError(f"Euler angle unit {self.euler_angles} is undefined")
        if self.temp not in reg_vals.TEMP_UNIT.keys():
            raise ValueError(f"Temperature unit {self.temp} is undefined.")
        if self.fus_data not in reg_vals.FUS_DATA_CONV.keys():
            raise ValueError(f"Orientation convention {self.fus_data} is undefined.")
        register_value = (reg_vals.FUS_DATA_CONV[self.fus_data] << 7)
        register_value |= (reg_vals.TEMP_UNIT[self.temp] << 4)
        register_value |= (reg_vals.EUL_ANG_UNIT[self.euler_angles] << 2)
        register_value |= (reg_vals.GYR_UNIT[self.gyr] << 1)
        register_value |= (reg_vals.ACC_UNIT[self.acc])
        return register_value
        

@dataclass
class BNO055Config:
    power_mode: reg_vals.PwrMode = reg_vals.PwrMode.NORMAL
    operation_mode: reg_vals.OpMode = reg_vals.OpMode.ACCGYRO
    accelerometer: BNO055AccConfig = field(default_factory=lambda: BNO055AccConfig())
    gyroscope: BNO055GyrConfig = field(default_factory=lambda: BNO055GyrConfig())
    unit: BNO055UnitConfig = field(default_factory=lambda: BNO055UnitConfig())
