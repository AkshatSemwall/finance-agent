import pytest
from unittest.mock import Mock, patch

from app.agent import FinanceAgent
from app.memory.manager import MemoryManager
from app.memory.json_memory import JsonLongTermMemory
from app.config import Settings

class TestFinanceAgent:
    def test_init(self):
        settings = Settings(openai_api_key="test", model="test")
        memory_manager = MemoryManager(JsonLongTermMemory())
        agent = FinanceAgent(memory_manager, settings)
        assert agent.memory_manager == memory_manager
        assert agent.settings == settings

    def test_build_messages(self):
        settings = Settings(openai_api_key="test", model="test")
        memory_manager = MemoryManager(JsonLongTermMemory())
        memory_manager.add_message("user", "Hello")
        agent = FinanceAgent(memory_manager, settings)
        messages = agent._build_messages()
        assert len(messages) == 2  # system + user
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Hello"

    @patch('app.agent.openai.OpenAI')
    def test_chat_no_tools(self, mock_openai):
        settings = Settings(openai_api_key="test", model="test")
        memory_manager = MemoryManager(JsonLongTermMemory())
        agent = FinanceAgent(memory_manager, settings)
        
        mock_client = Mock()
        mock_response = Mock()
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_message.tool_calls = None
        mock_response.choices = [Mock(message=mock_message)]
        mock_client.chat.completions.create.return_value = mock_response
        agent.client = mock_client
        
        response = agent.chat("Test message")
        assert response == "Test response"
        assert len(memory_manager.get_history()) == 2  # user + assistant

    def test_execute_tool_known(self):
        settings = Settings(openai_api_key="test", model="test")
        memory_manager = MemoryManager(JsonLongTermMemory())
        agent = FinanceAgent(memory_manager, settings)
        
        # Mock the function
        agent.tools['test_tool'] = lambda: "result"
        result = agent._execute_tool('test_tool', {})
        assert result == "result"

    def test_execute_tool_unknown(self):
        settings = Settings(openai_api_key="test", model="test")
        memory_manager = MemoryManager(JsonLongTermMemory())
        agent = FinanceAgent(memory_manager, settings)
        
        result = agent._execute_tool('unknown', {})
        assert result == {"error": "Tool unknown not found"}