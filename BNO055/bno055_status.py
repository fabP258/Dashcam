from dataclasses import dataclass, fields
from bno055_config import map_key_to_value

CALIBRATION_STATUS_MAP = {"NOT_CALIBRATED": 0x0, "FULLY_CALIBRATED": 0x3}


@dataclass
class BNO055CalibrationStatus:

    # TODO: check if given arguments are valid keys
    mag: str = None
    acc: str = None
    gyr: str = None
    sys: str = None

    @classmethod
    def from_register_value(cls, register_value: int):
        return cls(
            mag=map_key_to_value(CALIBRATION_STATUS_MAP, (register_value & 0b11)),
            acc=map_key_to_value(CALIBRATION_STATUS_MAP, (register_value >> 2) & 0b11),
            gyr=map_key_to_value(CALIBRATION_STATUS_MAP, (register_value >> 4) & 0b11),
            sys=map_key_to_value(CALIBRATION_STATUS_MAP, (register_value >> 6) & 0b11),
        )

    def print_status(self):
        # TODO: check validity
        print(f"==== {self.__class__.__name__} ====")
        for field in fields(self):
            print(f"{field.name}: {getattr(self, field.name)}")
