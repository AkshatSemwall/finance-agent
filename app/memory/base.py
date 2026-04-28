from abc import ABC, abstractmethod
from typing import Any

class BaseLongTermMemory(ABC):
    @abstractmethod
    def save(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass