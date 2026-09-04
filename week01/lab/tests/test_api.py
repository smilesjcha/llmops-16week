import json
from pathlib import Path

import httpx
from app.main import create_app
from app.providers import OllamaProvider, ProviderError
from fastapi.testclient import TestClient


def make_client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(log_path=tmp_path / "traces.jsonl"))


def test_health_and_frontend(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        health = client.get("/health")
        page = client.get("/")

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert page.status_code == 200
    assert "TRACE/01" in page.text
    assert "LLMOPS · INTEGRATED COURSE · WEEK 01" in page.text


def test_demo_generation_creates_privacy_safe_trace(tmp_path: Path) -> None:
    secret_input = "배송은 빠르지만 추천 결과의 근거를 알 수 없어 불편합니다."
    with make_client(tmp_path) as client:
        response = client.post(
            "/api/v1/generate",
            json={"text": secret_input, "task": "extract", "provider": "demo"},
        )
        traces = client.get("/api/v1/traces").json()
        stats = client.get("/api/v1/stats").json()

    assert response.status_code == 200
    assert response.json()["trace"]["prompt_version"] == "w01.signal.v1"
    assert response.json()["trace"]["provider"] == "demo"
    assert response.json()["trace"]["temperature"] == 0.2
    assert response.json()["trace"]["thinking_requested"] is False
    assert len(traces) == 1
    assert traces[0]["content_fingerprint"]
    assert secret_input not in (tmp_path / "traces.jsonl").read_text(encoding="utf-8")
    assert stats["total_requests"] == 1
    assert stats["success_rate"] == 1.0


def test_demo_extract_is_structured_distinct_and_deterministic(tmp_path: Path) -> None:
    text = "배송은 빨랐지만 추천 결과가 매번 달라서 비교하기 어려웠습니다."
    with make_client(tmp_path) as client:
        low_temperature = client.post(
            "/api/v1/generate",
            json={"text": text, "task": "extract", "provider": "demo", "temperature": 0.0},
        )
        high_temperature = client.post(
            "/api/v1/generate",
            json={"text": text, "task": "extract", "provider": "demo", "temperature": 1.0},
        )

    output = low_temperature.json()["output"]
    assert low_temperature.status_code == 200
    assert output == high_temperature.json()["output"]
    assert "SIGNAL — 배송은 빨랐다는 관찰" in output
    assert "FRICTION — 추천 결과가 매번 달라서 비교하기 어려웠습니다." in output
    assert "NEXT ACTION —" in output


def test_validation_rejects_unknown_fields(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        response = client.post(
            "/api/v1/generate",
            json={
                "text": "valid input",
                "task": "summarize",
                "provider": "demo",
                "api_key": "must-not-be-accepted",
            },
        )

    assert response.status_code == 422


def test_metrics_are_prometheus_readable(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        client.post(
            "/api/v1/generate",
            json={"text": "운영 가능한 최소 서비스", "task": "rewrite"},
        )
        response = client.get("/metrics")

    assert response.status_code == 200
    assert "trace01_requests_total 1" in response.text
    assert "trace01_latency_p95_ms" in response.text


def test_runtime_config_reports_fast_classroom_defaults(tmp_path: Path, monkeypatch) -> None:
    for name in (
        "OLLAMA_BASE_URL",
        "OLLAMA_MODEL",
        "OLLAMA_THINK",
        "OLLAMA_NUM_CTX",
        "OLLAMA_NUM_PREDICT",
        "OLLAMA_KEEP_ALIVE",
        "OLLAMA_SEED",
    ):
        monkeypatch.delenv(name, raising=False)

    with make_client(tmp_path) as client:
        response = client.get("/api/v1/config")

    assert response.status_code == 200
    assert response.json()["ollama"] == {
        "base_url": "http://127.0.0.1:11434",
        "model": "qwen3:4b-instruct",
        "thinking_requested": False,
        "num_ctx": 2048,
        "num_predict": 128,
        "keep_alive": "30m",
        "seed": 42,
    }


def test_ollama_request_disables_thinking_and_records_runtime_metrics(tmp_path: Path) -> None:
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured.update(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                "message": {"role": "assistant", "content": "핵심 결과"},
                "done": True,
                "done_reason": "stop",
                "load_duration": 125_000_000,
                "eval_duration": 250_000_000,
                "eval_count": 18,
            },
        )

    app = create_app(log_path=tmp_path / "traces.jsonl")
    app.state.providers["ollama"] = OllamaProvider(
        base_url="http://ollama.test",
        model="qwen3:4b-instruct",
        thinking_requested=False,
        num_ctx=2048,
        num_predict=128,
        keep_alive="30m",
        seed=42,
        transport=httpx.MockTransport(handler),
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/generate",
            json={"text": "합성 고객 피드백", "task": "summarize", "provider": "ollama"},
        )

    assert response.status_code == 200
    assert captured["think"] is False
    assert captured["keep_alive"] == "30m"
    assert captured["options"] == {
        "temperature": 0.2,
        "num_ctx": 2048,
        "num_predict": 128,
        "seed": 42,
    }
    trace = response.json()["trace"]
    assert trace["model"] == "qwen3:4b-instruct"
    assert trace["thinking_requested"] is False
    assert trace["output_token_limit"] == 128
    assert trace["model_load_ms"] == 125.0
    assert trace["model_generation_ms"] == 250.0
    assert trace["model_output_tokens"] == 18
    assert trace["finish_reason"] == "stop"


def test_provider_failure_returns_503_and_keeps_error_trace(tmp_path: Path) -> None:
    class FailingProvider:
        model = "missing-model"
        thinking_requested = False
        num_predict = 128

        async def generate(self, text: str, task: str, temperature: float) -> None:
            raise ProviderError("의도적으로 만든 연결 실패")

    app = create_app(log_path=tmp_path / "traces.jsonl")
    app.state.providers["ollama"] = FailingProvider()
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/generate",
            json={"text": "합성 입력", "task": "summarize", "provider": "ollama"},
        )
        traces = client.get("/api/v1/traces").json()

    assert response.status_code == 503
    assert traces[0]["status"] == "error"
    assert traces[0]["model"] == "missing-model"
    assert traces[0]["thinking_requested"] is False
    assert traces[0]["output_token_limit"] == 128
    assert traces[0]["error_type"] == "ProviderError"
    assert traces[0]["output_chars"] == 0
