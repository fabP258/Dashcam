from dataclasses import dataclass, field, fields
import recorder.BNO055.bno055_register_values as reg_vals
from abc import ABC, abstractmethod


def map_key_to_value(d: dict, value):
    """Returns the dictionary key corresponding to a given value. Assumes values to be unique in the dictionary."""
    res = None
    for k, v in d.items():
        if v == value:
            res = k
    return res


@dataclass
class BNO055ConfigBase(ABC):
    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_register_value(cls, register_value: int):
        raise NotImplementedError

    def print_config(self):
        """Prints the config to the console if the config is valid."""
        if not self.is_valid():
            raise ValueError(f"Cannot print an invalid {self.__class__.__name__}.")
        print(f"==== {self.__class__.__name__} ====")
        for f in fields(self):
            print(f"{f.name}: {getattr(self, f.name)}")


@dataclass
class BNO055AccConfig(BNO055ConfigBase):
    value_range: str = "4G"
    bandwidth: str = "62.5Hz"
    op_mode: str = "Normal"

    def get_register_value(self):
        if self.value_range not in reg_vals.ACC_G_RANGE.keys():
            raise ValueError(
                f"Accelerometer value range {self.value_range} not supported by sensor."
            )
        if self.bandwidth not in reg_vals.ACC_BANDWIDTH.keys():
            raise ValueError(
                f"Accelerometer bandwidth {self.bandwidth} not supported by sensor."
            )
        if self.op_mode not in reg_vals.ACC_OP_MODE.keys():
            raise ValueError(
                f"Accelerometer operation mode {self.op_mode} not supported by sensor."
            )
        return reg_vals.compose_acc_config(
            reg_vals.ACC_G_RANGE[self.value_range],
            reg_vals.ACC_BANDWIDTH[self.bandwidth],
            reg_vals.ACC_OP_MODE[self.op_mode],
        )

    def is_valid(self) -> bool:
        """Checks if the config is valid and returns the validity flag."""
        if not all([getattr(self, f.name) is not None for f in fields(self)]):
            return False
        if not self.value_range in reg_vals.ACC_G_RANGE.keys():
            return False
        if not self.bandwidth in reg_vals.ACC_BANDWIDTH.keys():
            return False
        if not self.op_mode in reg_vals.ACC_OP_MODE.keys():
            return False
        return True

    @classmethod
    def from_register_value(cls, register_value: int):
        """Creates an instance of the class from the read register value given as int."""
        rightmost_byte = register_value & 0xFF
        return cls(
            value_range=map_key_to_value(reg_vals.ACC_G_RANGE, rightmost_byte & 0b11),
            bandwidth=map_key_to_value(
                reg_vals.ACC_BANDWIDTH, (rightmost_byte >> 2) & 0b111
            ),
            op_mode=map_key_to_value(
                reg_vals.ACC_OP_MODE, (rightmost_byte >> 5) & 0b11100000
            ),
        )


@dataclass
class BNO055GyrConfig(BNO055ConfigBase):
    value_range: str = "2000dps"
    bandwidth: str = "32Hz"
    op_mode: str = "Normal"

    # TODO: Config is splitted into two registers, account for this
    def get_register_value_0(self):
        if self.value_range not in reg_vals.GYR_RANGE.keys():
            raise ValueError(
                f"Gyroscope value range {self.value_range} not supported by sensor."
            )
        if self.bandwidth not in reg_vals.GYR_BANDWIDTH.keys():
            raise ValueError(
                f"Gyroscope bandwidth {self.bandwidth} not supported by sensor."
            )
        # NOTE: Here only 6 Bits are returned since bit7 and bit6 are reserved
        return (reg_vals.GYR_BANDWIDTH[self.bandwidth] << 3) | reg_vals.GYR_RANGE[
            self.value_range
        ]

    def get_register_value_1(self):
        if self.op_mode not in reg_vals.GYR_OP_MODE.keys():
            raise ValueError(
                f"Gyroscope operation mode {self.op_mode} not supported by sensor."
            )
        # NOTE: Here only 3 Bits are returned since bit3 to bit7 are reserved
        return reg_vals.GYR_OP_MODE[self.op_mode]

    def is_valid(self) -> bool:
        if not all([getattr(self, f.name) is not None for f in fields(self)]):
            return False
        if not self.value_range in reg_vals.GYR_RANGE.keys():
            return False
        if not self.bandwidth in reg_vals.GYR_BANDWIDTH.keys():
            return False
        if not self.op_mode in reg_vals.GYR_OP_MODE.keys():
            return False
        return True

    @classmethod
    def from_register_value(cls, register_value0: int, register_value1):
        rightmost_byte0 = register_value0 & 0xFF
        rightmost_byte1 = register_value1 & 0xFF
        return cls(
            value_range=map_key_to_value(reg_vals.GYR_RANGE, rightmost_byte0 & 0b111),
            bandwidth=map_key_to_value(
                reg_vals.GYR_BANDWIDTH, (rightmost_byte0 >> 3) & 0b111
            ),
            op_mode=map_key_to_value(reg_vals.GYR_OP_MODE, rightmost_byte1 & 0b111),
        )


@dataclass
class BNO055UnitConfig(BNO055ConfigBase):
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
        register_value = reg_vals.FUS_DATA_CONV[self.fus_data] << 7
        register_value |= reg_vals.TEMP_UNIT[self.temp] << 4
        register_value |= reg_vals.EUL_ANG_UNIT[self.euler_angles] << 2
        register_value |= reg_vals.GYR_UNIT[self.gyr] << 1
        register_value |= reg_vals.ACC_UNIT[self.acc]
        return register_value

    def is_valid(self) -> bool:
        if not all([getattr(self, f.name) is not None for f in fields(self)]):
            return False
        if not self.acc in reg_vals.ACC_UNIT.keys():
            return False
        if not self.gyr in reg_vals.GYR_UNIT.keys():
            return False
        if not self.euler_angles in reg_vals.EUL_ANG_UNIT.keys():
            return False
        if not self.temp in reg_vals.TEMP_UNIT.keys():
            return False
        if not self.fus_data in reg_vals.FUS_DATA_CONV.keys():
            return False
        return True

    @classmethod
    def from_register_value(cls, register_value: int):
        rightmost_byte = register_value & 0xFF
        return cls(
            acc=map_key_to_value(reg_vals.ACC_UNIT, rightmost_byte & 0b1),
            gyr=map_key_to_value(reg_vals.GYR_UNIT, (rightmost_byte >> 1) & 0b1),
            euler_angles=map_key_to_value(
                reg_vals.EUL_ANG_UNIT, (rightmost_byte >> 2) & 0b1
            ),
            temp=map_key_to_value(reg_vals.TEMP_UNIT, (rightmost_byte >> 4) & 0b1),
        )


@dataclass
class BNO055Config:
    power_mode: reg_vals.PwrMode = reg_vals.PwrMode.NORMAL
    operation_mode: reg_vals.OpMode = reg_vals.OpMode.ACCGYRO
    accelerometer: BNO055AccConfig = field(default_factory=lambda: BNO055AccConfig())
    gyroscope: BNO055GyrConfig = field(default_factory=lambda: BNO055GyrConfig())
    unit: BNO055UnitConfig = field(default_factory=lambda: BNO055UnitConfig())
