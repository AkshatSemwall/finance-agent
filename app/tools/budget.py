import json
from typing import Dict, Any

from app.config import settings

def set_budget(category: str, amount: float) -> str:
    # Store in memory.json or something, but since memory is separate, perhaps use a budgets file or in memory.
    # For simplicity, use a budgets.json
    budgets = _load_budgets()
    budgets[category] = amount
    _save_budgets(budgets)
    return f"Budget for {category} set to ${amount}"

def check_budget(category: str) -> Dict[str, Any]:
    budgets = _load_budgets()
    transactions = _load_transactions()
    budget = budgets.get(category, 0)
    spent = sum(t['amount'] for t in transactions if t['category'] == category and t['amount'] < 0)
    spent = abs(spent)
    remaining = budget - spent
    return {
        "category": category,
        "budget": budget,
        "spent": spent,
        "remaining": remaining
    }

def _load_budgets() -> Dict[str, float]:
    budgets_file = "data/budgets.json"
    try:
        with open(budgets_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def _save_budgets(budgets: Dict[str, float]) -> None:
    budgets_file = "data/budgets.json"
    with open(budgets_file, 'w') as f:
        json.dump(budgets, f, indent=2)

def _load_transactions() -> list:
    try:
        with open(settings.transactions_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# OpenAI tool schemas
set_budget_tool_schema = {
    "type": "function",
    "function": {
        "name": "set_budget",
        "description": "Set a budget for a specific category.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "The category to set budget for"},
                "amount": {"type": "number", "description": "The budget amount in USD"}
            },
            "required": ["category", "amount"]
        }
    }
}

check_budget_tool_schema = {
    "type": "function",
    "function": {
        "name": "check_budget",
        "description": "Check the budget status for a specific category, including spent and remaining.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "The category to check budget for"}
            },
            "required": ["category"]
        }
    }
}