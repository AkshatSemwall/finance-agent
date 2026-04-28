from fastapi import APIRouter, Request
from typing import Dict, Any
from datetime import datetime, timedelta
import json

from app.config import settings

router = APIRouter()

@router.get("/insights/weekly")
async def get_weekly_insights(request: Request) -> Dict[str, Any]:
    transactions = _load_transactions()
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    weekly_transactions = [t for t in transactions if datetime.fromisoformat(t['date']) >= week_ago]
    total_spent = sum(abs(t['amount']) for t in weekly_transactions if t['amount'] < 0)
    by_category = {}
    for t in weekly_transactions:
        if t['amount'] < 0:
            cat = t['category']
            by_category[cat] = by_category.get(cat, 0) + abs(t['amount'])
    return {
        "total_spent": total_spent,
        "by_category": by_category,
        "transaction_count": len(weekly_transactions)
    }

def _load_transactions() -> list:
    try:
        with open(settings.transactions_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
