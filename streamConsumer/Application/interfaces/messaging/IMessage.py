from abc import ABC, abstractmethod


class IMessage(ABC):
    @abstractmethod
    def pack(self) -> bytes:
        pass
