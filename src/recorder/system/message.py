from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray


class Message(ABC):

    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def to_bytes(self) -> NDArray[np.int32]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_bytes(cls):
        raise NotImplementedError
