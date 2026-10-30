import asyncio
from dataclasses import replace
import json

import httpx
import pytest
from fastapi.testclient import TestClient

from week09.lab.app import create_app
from week09.lab.benchmark import run_load, summarize
from week09.lab.service import ChatRequest, Service, Settings, TTLCache, TokenBucket, cache_key


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"message": ""},
        {"message": "   "},
        {"message": "a" * 1001},
        {"message": "x", "max_tokens": 129},
        {"message": "x", "max_tokens": "64"},
        {"message": "x", "unknown": True},
    ],
)
def test_contract_rejection(payload):
    with TestClient(create_app()) as client:
        response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
    assert all("input" not in e for e in response.json()["error"]["fields"])


def test_success_cache_and_privacy():
    app = create_app()
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/ready").json()["ready"]
        a = client.post("/api/v1/chat", json={"message": "synthetic-secret-marker"})
        b = client.post("/api/v1/chat", json={"message": "synthetic-secret-marker"})
        assert not a.json()["cached"] and b.json()["cached"]
        assert a.json()["request_id"] != b.json()["request_id"]
        assert a.headers["x-request-id"] == a.json()["request_id"]
        stats = client.get("/lab/stats").json()
        assert stats["provider_calls"] == 1 and stats["active"] == 0
        assert "synthetic-secret-marker" not in json.dumps(stats)
        schema = client.get("/openapi.json").json()
        assert "ChatResponse" in schema["components"]["schemas"]


def test_faults_and_release():
    with TestClient(create_app(Settings(timeout_s=0.02))) as client:
        for scenario, status in [("timeout", 504), ("upstream_error", 502)]:
            r = client.post("/api/v1/chat", json={"message": "x", "scenario": scenario})
            assert r.status_code == status
            assert client.get("/lab/stats").json()["active"] == 0


def test_ttl_and_eviction():
    now = [0.0]
    cache = TTLCache(2, 2, clock=lambda: now[0])
    cache.set("a", "A")
    cache.set("b", "B")
    assert cache.get("a") == "A"
    cache.set("c", "C")
    assert cache.get("b") is None
    now[0] = 2
    assert cache.get("a") is None


def test_token_refill():
    now = [0.0]
    bucket = TokenBucket(2, 2, clock=lambda: now[0])
    assert bucket.allow() and bucket.allow() and not bucket.allow()
    now[0] = 0.5
    assert bucket.allow() and not bucket.allow()


def test_cache_version_scope():
    req = ChatRequest(message="x")
    cfg = Settings()
    assert cache_key(req, cfg) != cache_key(req, replace(cfg, prompt_version="v2"))
    assert cache_key(req, cfg) != cache_key(req.model_copy(update={"max_tokens": 32}), cfg)


def test_admission_timeout_and_cancel():
    async def check():
        app = create_app(Settings(max_inflight=1, mock_delay_s=0.1, timeout_s=0.3))
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://lab"
        ) as client:
            first = asyncio.create_task(
                client.post("/api/v1/chat", json={"message": "x", "use_cache": False})
            )
            while app.state.service.active == 0:
                await asyncio.sleep(0.001)
            second = await client.post("/api/v1/chat", json={"message": "y"})
            assert second.status_code == 503 and second.headers["retry-after"] == "1"
            assert (await first).status_code == 200
        service = Service(Settings(mock_delay_s=0.2, timeout_s=1))
        task = asyncio.create_task(service.chat(ChatRequest(message="x"), "cancel-test"))
        await asyncio.sleep(0.001)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert service.active == 0 and service.traces[-1]["status"] == "cancelled"

    asyncio.run(check())


def test_rate_status():
    with TestClient(create_app(Settings(burst=1, rate_per_s=0.001))) as client:
        assert client.post("/api/v1/chat", json={"message": "x"}).status_code == 200
        assert client.post("/api/v1/chat", json={"message": "x"}).status_code == 429


@pytest.mark.parametrize(
    "scenario,last", [("normal", "done"), ("timeout", "error"), ("upstream_error", "error")]
)
def test_stream_envelope(scenario, last):
    cfg = Settings(mock_delay_s=0.001, timeout_s=0.03)
    with TestClient(create_app(cfg)) as client:
        response = client.post("/api/v1/chat/stream", json={"message": "x", "scenario": scenario})
        assert response.status_code == 200
        events = [part.splitlines()[0] for part in response.text.strip().split("\n\n")]
        assert events[0] == "event: meta" and events[-1] == f"event: {last}"
        assert client.get("/lab/stats").json()["active"] == 0
        if last == "error":
            assert "event: done" not in response.text


def test_stream_capacity_release_when_closed():
    class Request:
        async def is_disconnected(self):
            return False

    async def check():
        service = Service(Settings(mock_delay_s=0.001))
        service.admit()
        gen = service.stream(ChatRequest(message="x"), "close", Request())
        await anext(gen)
        await gen.aclose()
        assert service.active == 0

    asyncio.run(check())


@pytest.mark.parametrize(
    "status,expected,code",
    [(404, 502, "model_not_found"), (500, 502, "upstream_error"), (200, 200, None)],
)
def test_ollama_mapping(status, expected, code):
    def handler(request):
        if request.url.path == "/api/tags":
            return httpx.Response(200, json={"models": [{"name": "installed:test"}]})
        body = json.loads(request.content)
        assert body["think"] is False and body["stream"] is False
        return httpx.Response(status, json={"message": {"content": "합성 모의 응답"}})

    app = create_app(
        Settings(provider="ollama", model="installed:test"), transport=httpx.MockTransport(handler)
    )
    with TestClient(app) as client:
        assert client.get("/ready").status_code == 200
        response = client.post("/api/v1/chat", json={"message": "x"})
        assert response.status_code == expected
        if code:
            assert response.json()["error"]["code"] == code
        assert client.post("/api/v1/chat/stream", json={"message": "x"}).status_code == 409


def test_ollama_unavailable_and_missing():
    def handler(request):
        raise httpx.ConnectError("synthetic private upstream detail")

    app = create_app(
        Settings(provider="ollama", model="missing"), transport=httpx.MockTransport(handler)
    )
    with TestClient(app) as client:
        assert client.get("/ready").status_code == 503
        r = client.post("/api/v1/chat", json={"message": "x"})
        assert r.status_code == 503
        assert "private upstream" not in r.text


def test_load_and_quantiles():
    result = summarize([{"status": 200, "elapsed_ms": 10}, {"status": 503, "elapsed_ms": 1}], 1)
    assert result["success_latency_ms"]["p50"] == 10 and result["error_rate"] == 0.5
    assert result["successful_rps"] == 1 and result["completed_rps"] == 2
    assert summarize([{"status": 503, "elapsed_ms": 1}], 1)["success_latency_ms"]["p99"] is None

    async def check():
        app = create_app(Settings(mock_delay_s=0.001))
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://lab"
        ) as client:
            report = await run_load(client, n=8, concurrency=2)
            assert report["summary"]["success"] == 8
            with pytest.raises(ValueError):
                await run_load(client, n=1000)

    asyncio.run(check())


@pytest.mark.parametrize(
    "change",
    [
        {"timeout_s": 0},
        {"mock_delay_s": -1},
        {"rate_per_s": float("nan")},
        {"max_inflight": 0},
        {"provider": "unknown"},
        {"max_inflight": 1.5},
        {"prompt_version": "unknown"},
    ],
)
def test_invalid_settings(change):
    with pytest.raises(ValueError):
        Settings(**change)
