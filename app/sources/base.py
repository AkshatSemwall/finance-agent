from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseTransactionSource(ABC):
    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        pass