from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def read(self, path: str) -> bytes:
        pass

    @abstractmethod
    def write(self, path: str, data: bytes) -> None:
        pass
