"""Tests for {{ name }}"""

import pytest
from fastapi.testclient import TestClient

from agent import {{ class_name }}Agent

@pytest.fixture
def agent():
    return {{ class_name }}Agent()

def test_agent_initializes(agent):
    """Test agent creates successfully"""
    assert agent.app is not None
    assert len(agent.conversation_history) == 0

def test_root_endpoint(agent):
    """Test root endpoint returns agent info"""
    client = TestClient(agent.app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "agent" in data
    assert "provider" in data

def test_health_endpoint(agent):
    """Test health endpoint"""
    client = TestClient(agent.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_clear_history(agent):
    """Test clearing history"""
    agent.conversation_history = [{"role": "user", "content": "test"}]
    client = TestClient(agent.app)
    response = client.post("/clear")
    assert response.status_code == 200
    assert len(agent.conversation_history) == 0
