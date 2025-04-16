import os
import pytest
from fastapi.testclient import TestClient

import app


# Setup a test client with environment variables
@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("SERVER_API_KEY", "testkey")
    monkeypatch.setenv("CENSUS_API_KEY", "dummykey")
    yield


client = TestClient(app.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_initialize():
    payload = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
    response = client.post("/", json=payload, headers={"X-API-Key": "testkey"})
    assert response.status_code == 200
    data = response.json()
    assert data.get("result", {}).get("protocolVersion") == "2025-03-26"


def test_tools_list():
    payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    response = client.post("/", json=payload, headers={"X-API-Key": "testkey"})
    data = response.json()
    tools = data.get("result", {}).get("tools", [])
    assert isinstance(tools, list)
    assert tools[0]["name"] == "census/get"


def test_tools_call_missing_params():
    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "census/get", "arguments": {}},
    }
    response = client.post("/", json=payload, headers={"X-API-Key": "testkey"})
    data = response.json()
    assert data.get("error", {}).get("code") == -32602
