import json
from typing import Dict, Any

from app.config import settings

def get_spending_summary() -> Dict[str, Any]:
    transactions = _load_transactions()
    total = sum(t['amount'] for t in transactions if t['amount'] < 0)  # negative amounts are spending
    by_category = {}
    for t in transactions:
        if t['amount'] < 0:
            cat = t['category']
            by_category[cat] = by_category.get(cat, 0) + t['amount']
    return {
        "total_spent": abs(total),
        "by_category": {k: abs(v) for k, v in by_category.items()}
    }

def _load_transactions() -> list:
    try:
        with open(settings.transactions_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# OpenAI tool schema
spending_tool_schema = {
    "type": "function",
    "function": {
        "name": "get_spending_summary",
        "description": "Get a summary of spending, including total spent and breakdown by category.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}