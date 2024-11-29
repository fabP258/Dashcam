from abc import abstractmethod
from multiprocessing import Condition, shared_memory
from multiprocessing.shared_memory import SharedMemory
from typing import Optional

import numpy as np

from recorder.system.process import PythonProcess


class SharedMemory(PythonProcess):
    def __init__(self, start_time: float, shm_name: str, shm_size: int, shm_condition: Condition):  # type: ignore
        super().__init__(start_time)
        self.shm_name: str = shm_name
        self.shm_size: int = shm_size
        self.shm: Optional[SharedMemory] = None
        self.shm_buffer: Optional[np.ndarray] = None
        self.shm_condition: Optional[Condition] = shm_condition  # type: ignore

    @abstractmethod
    def setup_shm(self):
        """Setup the shared memory and the buffer to the shared memory."""
        pass

    def close(self):
        """Close the shared memory."""
        self.shm.close()


class SharedMemoryPublisher(SharedMemory):
    def __init__(self, start_time: float, shm_name: str, shm_size: int, shm_condition):
        super().__init__(start_time, shm_name, shm_size, shm_condition)
        self.setup_shm()

    def setup_shm(self):
        if self.shm is not None or self.shm_buffer is not None:
            assert False, "Shared memory already initialized"

        self.shm = shared_memory.SharedMemory(
            create=True, name=self.shm_name, size=self.shm_size
        )

    def publish(self, data: bytes):
        with self.shm_condition:
            if len(data) > self.shm_size:
                # what to do then?
                raise ValueError("Data size is greater than shared memory size")
            self.shm.buf[: len(data)] = data
            self.shm_condition.notify_all()


class SharedMemorySubscriber(SharedMemory):
    def __init__(self, start_time: float, shm_name: str, shm_size: int, shm_condition):
        super().__init__(start_time, shm_name, shm_size, shm_condition)
        self.setup_shm()

    def setup_shm(self):
        if self.shm is not None or self.shm_buffer is not None:
            assert False, "Shared memory already attached"

        self.shm = shared_memory.SharedMemory(name=self.shm_name)

    def subscribe(self):
        """Subscribe to the shared memory and return the data."""
        with self.shm_condition:
            self.shm_condition.wait()
            return bytes(self.shm.buf[:]).decode().split("\x00")[0]
