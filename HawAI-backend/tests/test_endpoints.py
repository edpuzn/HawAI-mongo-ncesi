import pytest
import httpx

from app.main import app


@pytest.mark.asyncio
async def test_healthz(monkeypatch):
    # Mock Ollama ping to True
    from app.services import ollama_client as oc

    async def fake_ping(self):
        return True

    monkeypatch.setattr(oc.OllamaClient, "ping", fake_ping)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/healthz")
    assert resp.status_code == 200
    js = resp.json()
    assert js.get("status") == "ok"
    assert "ollama" in js and isinstance(js["ollama"], dict)
    assert js["ollama"].get("reachable") is True
    assert isinstance(js["ollama"].get("host"), str)


@pytest.mark.asyncio
async def test_chat(mocked_generate_monkeypatch):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/chat", json={"message": "Merhaba"})
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data and isinstance(data["reply"], str)
    assert "sdg_tags" in data and isinstance(data["sdg_tags"], list)
    assert "sources" in data and isinstance(data["sources"], list) and len(data["sources"]) == 2
    assert "safety" in data and isinstance(data["safety"], dict)


@pytest.fixture
def mocked_generate_monkeypatch(monkeypatch):
    from app.services import ollama_client as oc

    async def fake_generate(self, prompt, user_meta=None):
        return "Test yanit"

    monkeypatch.setattr(oc.OllamaClient, "generate", fake_generate)
    return monkeypatch
