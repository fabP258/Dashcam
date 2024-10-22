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

@dataclass
class BNO055Config:
    power_mode: reg_vals.PwrMode = reg_vals.PwrMode.NORMAL
    operation_mode: reg_vals.OpMode = reg_vals.OpMode.ACCGYRO
    accelerometer: BNO055AccConfig = field(default_factory=lambda: BNO055AccConfig())
    gyroscope: BNO055GyrConfig = field(default_factory=lambda: BNO055GyrConfig())
