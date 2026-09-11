import pytest
from fastapi.testclient import TestClient
from prompt02.main import RUNS, app


@pytest.fixture
def client():
    RUNS.clear()
    with TestClient(app) as client:
        yield client


def test_health_catalog_and_ui(client):
    assert client.get("/health").json()["service"] == "PROMPT/02"
    catalog = client.get("/api/catalog").json()
    assert len(catalog["dataset"]["cases"]) == 8
    assert catalog["output_schema"]["additionalProperties"] is False
    page = client.get("/")
    assert page.status_code == 200
    assert "교육용 시뮬레이션" in page.text
    assert client.get("/static/app.js").status_code == 200


def test_preview_and_not_found(client):
    preview = client.get("/api/prompt/v3?case_id=T06").json()
    assert len(preview["messages"]) == 2
    assert client.get("/api/prompt/v0").status_code == 404
    assert client.get("/api/prompt/v3?case_id=NOPE").status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"provider": "paid-cloud"},
        {"versions": []},
        {"versions": ["v1", "v1"]},
        {"case_ids": []},
        {"case_ids": ["T01", "T01"]},
        {"input": "arbitrary PII"},
    ],
)
def test_api_rejects_unsupported_requests(client, payload):
    assert client.post("/api/experiments", json=payload).status_code == 422


def test_unknown_case_is_rejected(client):
    assert client.post("/api/experiments", json={"case_ids": ["UNKNOWN"]}).status_code == 400


def test_full_workflow_and_safe_export(client):
    report = client.post("/api/experiments", json={"provider": "demo"}).json()
    assert len(report["rows"]) == 24
    choice = client.post(
        "/api/decisions",
        json={
            "run_id": report["run_id"],
            "version": "v3",
            "reason": "복합 의도 문의의 분류를 개선했으며 새 데이터로 추가 평가할 예정입니다.",
        },
    )
    assert choice.status_code == 200
    assert choice.json()["deployed"] is False
    export = client.get(f"/api/experiments/{report['run_id']}/export")
    assert export.headers["content-disposition"].startswith("attachment;")
    assert export.json()["decisions"][0]["scope"] == "educational_candidate_only"
    assert client.get("/api/experiments/unknown/export").status_code == 404


def test_decision_requires_observed_version_and_reason(client):
    report = client.post("/api/experiments", json={"versions": ["v1"], "case_ids": ["T01"]}).json()
    payload = {
        "run_id": report["run_id"],
        "version": "v3",
        "reason": "평가되지 않은 후보를 선택하려는 테스트입니다.",
    }
    assert client.post("/api/decisions", json=payload).status_code == 400
    payload.update(version="v1", reason="짧음")
    assert client.post("/api/decisions", json=payload).status_code == 422
