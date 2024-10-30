import smbus2
from typing import List


class I2CSensor:
    def __init__(self, i2c_address: int, i2c_bus_identifier: int):
        self._i2c_address = i2c_address
        self._i2c_bus = smbus2.SMBus(i2c_bus_identifier)

    def read_byte_data(self, register: int) -> int:
        return self._i2c_bus.read_byte_data(self._i2c_address, register)

    def read_i2c_block_data(self, start_register: int, length: int) -> List[int]:
        return self._i2c_bus.read_i2c_block_data(
            self._i2c_address, start_register, length
        )

    def write_byte_data(self, register: int, value: int) -> None:
        self._i2c_bus.write_byte_data(self._i2c_address, register, value)
