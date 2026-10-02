"""Smoke tests for both offline teaching UIs, independent of a running server."""

import pytest
from fastapi.testclient import TestClient

from week04.lab.rag04.main import app as week04_app
from week05.lab.search05.main import app as week05_app


@pytest.mark.parametrize("week,app", [(4, week04_app), (5, week05_app)])
def test_lab_health_and_home(week, app):
    client = TestClient(app)
    assert client.get("/health").json() == {
        "status": "ok",
        "week": week,
        "mode": "offline",
        "synthetic_data": True,
    }
    page = client.get("/")
    assert page.status_code == 200
    assert "text/html" in page.headers["content-type"]


@pytest.mark.parametrize("app", [week04_app, week05_app])
def test_lab_search_and_evaluation(app):
    client = TestClient(app)
    request = {"query": "상품 반품 기간", "method": "bm25"}
    search = client.post("/api/search", json=request)
    assert search.status_code == 200
    report = search.json()
    assert report["query"] == request["query"]
    assert report["hits"]
    assert "answer" in report

    evaluation = client.post("/api/evaluate", json=request)
    assert evaluation.status_code == 200
    assert "summary" in evaluation.json()
    assert "rows" in evaluation.json()


@pytest.mark.parametrize("app", [week04_app, week05_app])
def test_lab_invalid_input_is_rejected(app):
    client = TestClient(app)
    assert client.post("/api/search", json={"query": ""}).status_code == 422
    assert client.post("/api/search", json={"query": "상품 반품 기간", "role": "admin"}).status_code == 422
    assert client.post("/api/search", json={"query": "상품 반품 기간", "size": 30, "overlap": 30}).status_code == 422
