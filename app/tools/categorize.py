import json
from typing import Dict, Any

from app.config import settings

def auto_categorize(description: str, amount: float) -> str:
    # Simple rule-based categorization
    desc_lower = description.lower()
    if any(word in desc_lower for word in ['coffee', 'starbucks', 'mcdonald', 'restaurant', 'food', 'grocery', 'chipotle', 'pizza', 'burger', 'taco', 'sushi', 'steak']):
        return 'food'
    elif any(word in desc_lower for word in ['gas', 'shell', 'fuel', 'uber', 'lyft', 'taxi', 'bus', 'train', 'transport', 'parking', 'toll', 'car']):
        return 'transport'
    elif any(word in desc_lower for word in ['electric', 'water', 'internet', 'gas bill', 'utility', 'bill']):
        return 'utilities'
    elif any(word in desc_lower for word in ['netflix', 'spotify', 'hbo', 'disney', 'game', 'movie', 'theater', 'concert', 'entertainment']):
        return 'entertainment'
    elif any(word in desc_lower for word in ['pharmacy', 'cvs', 'walgreens', 'doctor', 'dentist', 'health', 'gym', 'vitamin', 'massage']):
        return 'health'
    else:
        return 'uncategorized'

# OpenAI tool schema
categorize_tool_schema = {
    "type": "function",
    "function": {
        "name": "auto_categorize",
        "description": "Automatically categorize a transaction based on description and amount.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "The transaction description"},
                "amount": {"type": "number", "description": "The transaction amount"}
            },
            "required": ["description", "amount"]
        }
    }
}