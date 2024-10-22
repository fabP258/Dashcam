from enum import Enum

class OpMode(Enum):
    CONFIGMODE = 0x0
    # Non-Fusion modes
    ACCONLY = 0x1
    MAGONLY = 0x2
    GYROONLY = 0x3
    ACCMAG = 0x4
    ACCGYRO = 0x5
    MAGGYRO = 0x6
    AMG = 0x7
    # Fusion modes
    IMU = 0x8
    COMPASS = 0x9
    M4G = 0xA
    NDOF_FMC_OFF = 0xB
    NDOF = 0xC

class PwrMode(Enum):
    NORMAL = 0x0
    LOW_POWER = 0x1
    SUSPEND = 0x2

ACC_G_RANGE = {"2G": 0x0, "4G": 0x1, "8G": 0x2, "16G": 0x3}
ACC_BANDWIDTH = {"7.81Hz": 0x0, "15.63Hz": 0x1, "31.25Hz": 0x2, "62.5Hz": 0x3, "125Hz": 0x4, "250Hz": 0x5, "500Hz": 0x6, "1000Hz": 0x7}
ACC_OP_MODE = {"Normal": 0x0, "Suspend": 0x1, "LowPower1": 0x2, "Standby": 0x3, "LowPower2": 0x4, "DeepSuspend": 0x5}

def compose_acc_config(g_range: hex, bandwidth: hex, op_mode: hex):
    register_value = (op_mode << 5) | (bandwidth << 2) | g_range
    return register_value

GYR_RANGE = {"2000dps": 0x0, "1000dps": 0x1, "500dps": 0x2, "250dps": 0x3, "125dps": 0x4}
GYR_BANDWIDTH = {"523Hz": 0x0, "230Hz": 0x1, "116Hz": 0x2, "47Hz": 0x3, "23Hz": 0x4, "12Hz": 0x5, "64Hz": 0x6, "32Hz": 0x7}
GYR_OP_MODE = {"Normal": 0x0, "FastPowerUp": 0x1, "DeepSuspend": 0x2, "Suspend": 0x3, "AdvancedPowersave": 0x4}
