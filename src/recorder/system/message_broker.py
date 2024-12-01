import numpy as np
from multiprocessing import shared_memory, Lock

"""
To-do:
* Message class (to_bytes(), n_bytes, from_bytes(cls)), Protobuf?
* Handle has_new_data with deliver timestamp for each message --> maintain last timestamps in child message brokers?
"""


class SharedMemoryMessageBroker:

    def __init__(self, shm_name=None):
        self._lock = Lock()

        if shm_name is None:
            self._mem_buffer = shared_memory.SharedMemory(
                create=True, size=10 * np.dtype(np.int32).itemsize
            )
        else:
            self._mem_buffer = shared_memory.SharedMemory(name=shm_name)
        self._data = np.ndarray((10,), dtype=np.int32, buffer=self._mem_buffer.buf)
        self._data[:] = 0

        # TODO: generate slices based on a list of messages
        self._message_slices = {0: slice(0, 5), 1: slice(5, 10)}

        # TODO: track receive timestamps
        self._rec_timestamps = {0: None, 1: None}

    def publish(self, message_id: int, data: np.array):
        # TODO: take Message class object as arg
        if message_id not in self._message_slices:
            raise ValueError(f"Invalid message id ({message_id})")
        msg_slice = self._message_slices[message_id]

        # if len(data) > len(msg_slice):
        #    raise ValueError("Data is to large for allocated memory buffer")

        with self._lock:
            self._data[msg_slice] = data

    def receive(self, message_id: int):
        if message_id not in self._message_slices:
            raise ValueError(f"Invalid message id ({message_id})")
        msg_slice = self._message_slices[message_id]

        with self._lock:
            # TODO: convert to Message()
            return self._data[msg_slice]

    def shm_name(self):
        return self._mem_buffer.name
