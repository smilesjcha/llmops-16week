from pathlib import Path

from app.main import create_app
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
