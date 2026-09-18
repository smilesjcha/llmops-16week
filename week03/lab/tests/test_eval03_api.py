import pytest
from eval03.main import RUNS, app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    RUNS.clear()
    with TestClient(app) as client:
        yield client


def test_health_catalog_and_ui(client):
    assert client.get("/health").json()["service"] == "EVAL/03"
    catalog = client.get("/api/catalog").json()
    assert len(catalog["dataset"]["cases"]) == 6
    assert catalog["required_sections"] == ["결정 사항", "실행 항목", "위험·확인 필요", "다음 단계"]
    page = client.get("/")
    assert page.status_code == 200
    assert "고정 응답" in page.text


def test_rejects_unsupported_request_shape(client):
    unsupported_payloads = (
        {"split": "all"},
        {"versions": []},
        {"versions": ["v0.1", "v0.1"]},
        {"extra": True},
    )
    for payload in unsupported_payloads:
        assert client.post("/api/evaluations", json=payload).status_code == 422


def test_dev_and_test_reports_are_separate(client):
    dev = client.post("/api/evaluations", json={"split": "dev"}).json()
    test = client.post("/api/evaluations", json={"split": "test"}).json()
    assert len(dev["rows"]) == 8
    assert len(test["rows"]) == 4
    assert dev["summary"]["v0.1"]["overall_ok"]["passed"] == 0
    assert dev["summary"]["v0.2"]["overall_ok"]["passed"] == 2
    assert test["summary"]["v0.2"]["overall_ok"]["passed"] == 2
    assert dev["dataset_hash"] != test["dataset_hash"]


def test_decision_requires_observed_version_and_exports(client):
    report = client.post("/api/evaluations", json={"split": "dev", "versions": ["v0.2"]}).json()
    invalid = client.post(
        "/api/decisions",
        json={
            "run_id": report["run_id"],
            "version": "v0.1",
            "decision": "hold",
            "reason": "평가하지 않은 버전을 선택하려는 테스트 문장입니다.",
        },
    )
    assert invalid.status_code == 400
    saved = client.post(
        "/api/decisions",
        json={
            "run_id": report["run_id"],
            "version": "v0.2",
            "decision": "hold",
            "reason": "개발 사례의 오류를 확인했고 별도 확인 사례에서 다시 평가하겠습니다.",
        },
    )
    assert saved.status_code == 200
    assert saved.json()["deployed"] is False
    exported = client.get(f"/api/evaluations/{report['run_id']}/export")
    assert exported.status_code == 200
    assert exported.json()["decisions"][0]["decision"] == "hold"
