import pytest

pytestmark = pytest.mark.asyncio


async def test_register_and_login(client, monkeypatch):
    monkeypatch.setattr("app.workers.tasks.send_verification_email.delay", lambda *a, **k: None)
    r = await client.post("/api/v1/auth/register", json={
        "email": "a@b.com", "full_name": "Test", "password": "secret123"})
    assert r.status_code == 201

    r = await client.post("/api/v1/auth/login", data={
        "username": "a@b.com", "password": "secret123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


async def test_health(client):
    r = await client.get("/health")
    assert r.json()["status"] == "ok"
