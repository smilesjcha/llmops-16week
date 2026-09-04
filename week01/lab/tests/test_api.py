from pathlib import Path

from app.main import create_app
from app.providers import ProviderError
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


def test_provider_failure_returns_503_and_keeps_error_trace(tmp_path: Path) -> None:
    class FailingProvider:
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
    assert traces[0]["error_type"] == "ProviderError"
    assert traces[0]["output_chars"] == 0
