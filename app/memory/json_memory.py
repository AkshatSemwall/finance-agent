import json
import os
from typing import Any

from app.memory.base import BaseLongTermMemory
from app.config import settings

class JsonLongTermMemory(BaseLongTermMemory):
    def __init__(self):
        self.file_path = settings.memory_file
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def save(self, key: str, value: Any) -> None:
        data = self._load_data()
        data[key] = value
        self._save_data(data)

    def get(self, key: str) -> Any:
        data = self._load_data()
        return data.get(key)

    def clear(self) -> None:
        self._save_data({})

    def _load_data(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _save_data(self, data: dict) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)