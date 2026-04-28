from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.main import app

class TestEndpoints:
    def test_chat_endpoint(self):
        # Mock the agent
        mock_agent = Mock()
        mock_agent.chat.return_value = "Mocked response"
        app.state.agent = mock_agent
        
        client = TestClient(app)
        response = client.post("/chat", json={"message": "Hello"})
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Mocked response"

    def test_clear_memory(self):
        mock_agent = Mock()
        app.state.agent = mock_agent
        
        client = TestClient(app)
        response = client.delete("/memory")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Memory cleared successfully"

    def test_sync_transactions(self):
        mock_importer = Mock()
        app.state.csv_importer = mock_importer
        
        client = TestClient(app)
        response = client.post("/sync", json={"csv_path": "data/sample.csv"})
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_get_transactions(self):
        mock_importer = Mock()
        mock_importer.fetch.return_value = [{"date": "2024-01-01", "amount": -10}]
        app.state.csv_importer = mock_importer
        
        client = TestClient(app)
        response = client.get("/transactions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_insights(self):
        client = TestClient(app)
        response = client.get("/insights/weekly")
        assert response.status_code == 200
        data = response.json()
        assert "total_spent" in data
        assert "by_category" in data
        assert "transaction_count" in data