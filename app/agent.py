import json
from typing import Dict, Any, List

import openai

from app.config import settings
from app.memory.manager import MemoryManager
from app.tools.budget import set_budget, check_budget
from app.tools.categorize import auto_categorize
from app.tools.spending import get_spending_summary

SYSTEM_PROMPT = """
You are a personal finance assistant. You have access to the user's transaction history and budget goals.
Always answer in 2-3 sentences max unless the user asks for a detailed breakdown.
Use tools to fetch real numbers — never guess. Currency is USD.
If the user sets a budget goal, confirm it and store it.
"""

class FinanceAgent:
    def __init__(self, memory_manager: MemoryManager, settings: Any):
        self.memory_manager = memory_manager
        self.settings = settings
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.tools = {
            "get_spending_summary": get_spending_summary,
            "set_budget": set_budget,
            "check_budget": check_budget,
            "auto_categorize": auto_categorize,
        }
        self.tool_schemas = [
            {
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
            },
            {
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
            },
            {
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
            },
            {
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
        ]

    def chat(self, user_message: str) -> str:
        self.memory_manager.add_message("user", user_message)
        messages = self._build_messages()
        
        while True:
            response = self.client.chat.completions.create(
                model=self.settings.model,
                messages=messages,
                tools=self.tool_schemas,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            messages.append(assistant_message)
            
            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    result = self._execute_tool(function_name, arguments)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })
            else:
                # No more tool calls, final answer
                break
        
        reply = assistant_message.content
        self.memory_manager.add_message("assistant", reply)
        return reply

    def _build_messages(self) -> List[Dict[str, Any]]:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in self.memory_manager.get_history():
            messages.append(msg)
        return messages

    def _execute_tool(self, name: str, args: Dict[str, Any]) -> Any:
        if name in self.tools:
            return self.tools[name](**args)
        else:
            return {"error": f"Tool {name} not found"}