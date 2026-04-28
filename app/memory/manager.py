from typing import List, Dict, Any

from app.memory.base import BaseLongTermMemory

class MemoryManager:
    def __init__(self, long_term_memory: BaseLongTermMemory):
        self.short_term: Dict[str, Any] = {}
        self.long_term = long_term_memory

    def add_message(self, role: str, content: str) -> None:
        if 'history' not in self.short_term:
            self.short_term['history'] = []
        self.short_term['history'].append({'role': role, 'content': content})

    def get_history(self) -> List[Dict[str, str]]:
        return self.short_term.get('history', [])

    def set_goal(self, goal: str) -> None:
        goals = self.get_goals()
        goals.append(goal)
        self.long_term.save('goals', goals)

    def get_goals(self) -> List[str]:
        return self.long_term.get('goals') or []

    def clear(self) -> None:
        self.short_term.clear()
        self.long_term.clear()