import asyncio
from dataclasses import replace
import json
import pytest
from week10.lab.app import create_app
from week10.lab.config import Settings
from week10.lab.experiments import compare_releases, fixture_check, lab_client, window_delta
from week10.lab.telemetry import BUCKETS, trace_context


@pytest.mark.parametrize(
    "values",
    [
        {"release": "latest"},
        {"capacity": 0},
        {"capacity": True},
        {"capacity": 9},
        {"timeout_s": float("nan")},
        {"timeout_s": float("inf")},
        {"timeout_s": 0},
        {"emit_logs": 1},
    ],
)
def test_settings_reject(values):
    with pytest.raises(ValueError):
        Settings(**values)


def test_manifest_stable_and_sensitive():
    a = Settings()
    assert a.manifest() == Settings().manifest()
    assert a.manifest()["config_id"] != replace(a, timeout_s=0.5).manifest()["config_id"]
    assert "emit_logs" not in a.manifest()


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "00-" + "0" * 32 + "-" + "1" * 16 + "-01",
        "bad",
        "ff-" + "a" * 32 + "-" + "b" * 16 + "-01",
    ],
)
def test_bad_trace_renew(value):
    tid, parent = trace_context(value)
    assert len(tid) == 32 and int(tid, 16) > 0 and parent is None


def test_valid_trace():
    assert trace_context("00-" + "a" * 32 + "-" + "b" * 16 + "-01") == ("a" * 32, "b" * 16)


@pytest.mark.anyio
async def test_health_lifecycle():
    app = create_app(Settings())
    assert not app.state.started
    async with lab_client() as (app, c):
        assert (await c.get("/health/ready")).status_code == 200
        app.state.dependency_ok = False
        assert (await c.get("/health/live")).status_code == 200
        assert (await c.get("/health/ready")).status_code == 503
        assert (await c.post("/api/v1/assist", json={"message": "a"})).status_code == 503
    assert not app.state.started and app.state.draining


@pytest.mark.anyio
async def test_success_spans_and_context():
    async with lab_client() as (app, c):
        r = await c.post(
            "/api/v1/assist",
            json={"message": "hello"},
            headers={"traceparent": "00-" + "a" * 32 + "-" + "b" * 16 + "-01"},
        )
        assert r.status_code == 200 and r.json()["simulated"]
        spans = list(app.state.telemetry.spans)
        root = next(x for x in spans if x["name"] == "assist")
        assert root["parent_id"] == "b" * 16 and root["trace_id"] == "a" * 32
        assert all(x["parent_id"] == root["span_id"] for x in spans if x["name"] != "assist")
        assert r.headers["X-Trace-ID"] == r.json()["trace_id"] == "a" * 32
        assert fixture_check(r.json()["answer"])


@pytest.mark.parametrize(
    "scenario,status,step",
    [
        ("slow", 504, "generate"),
        ("retrieval_error", 502, "retrieve"),
        ("provider_error", 502, "generate"),
    ],
)
@pytest.mark.anyio
async def test_failures_release_capacity(scenario, status, step):
    async with lab_client() as (app, c):
        r = await c.post("/api/v1/assist", json={"message": "hello", "scenario": scenario})
        assert r.status_code == status and app.state.telemetry.active == 0
        assert any(s["name"] == step and s["status"] == "ERROR" for s in app.state.telemetry.spans)
        assert (await c.post("/api/v1/assist", json={"message": "hello"})).status_code == 200


@pytest.mark.parametrize(
    "body",
    [
        {"message": " "},
        {"message": 2},
        {"message": "x", "secret": "no"},
        {"message": "x", "scenario": "unknown"},
    ],
)
@pytest.mark.anyio
async def test_validation_private_and_counted(body):
    async with lab_client() as (app, c):
        r = await c.post("/api/v1/assist", json=body)
        assert r.status_code == 422
        assert app.state.telemetry.total == 1
        assert set(r.json()) == {"error", "request_id"} and "secret" not in r.text


@pytest.mark.anyio
async def test_concurrency_isolation_and_admission():
    async with lab_client(Settings(capacity=1)) as (app, c):
        rs = await asyncio.gather(
            *[c.post("/api/v1/assist", json={"message": f"x{i}"}) for i in range(4)]
        )
        assert sorted(r.status_code for r in rs) == [200, 503, 503, 503]
        assert len({r.headers["X-Trace-ID"] for r in rs}) == 4
        assert app.state.telemetry.active == 0
        logs = app.state.telemetry.logs
        assert all(
            s["trace_id"] in {r.headers["X-Trace-ID"] for r in rs}
            for s in app.state.telemetry.spans
        )
        assert len(logs) == 4


@pytest.mark.anyio
async def test_logs_exclude_payload_and_metrics_labels():
    async with lab_client(Settings(emit_logs=True)) as (app, c):
        await c.post("/api/v1/assist", json={"message": "SECRET-TEST-ONLY"})
        snap = (await c.get("/lab/snapshot")).json()
        metrics = (await c.get("/metrics")).text
        assert (
            "SECRET-TEST-ONLY" not in json.dumps(snap)
            and "request_id" not in metrics
            and "trace_id" not in metrics
        )
        assert snap["total"] == 1
        assert "lab_assist_duration_seconds_count 1" in metrics
        assert list(app.state.telemetry.buckets.values()) == sorted(
            app.state.telemetry.buckets.values()
        )
        assert app.state.telemetry.buckets[BUCKETS[-1]] == 1
        assert "lab_assist_active 0" in metrics


@pytest.mark.anyio
async def test_window_and_release_gate():
    rows = await compare_releases()
    assert [r["http_success"] for r in rows] == [4, 4]
    assert [r["fixture_pass"] for r in rows] == [4, 0]
    async with lab_client() as (app, c):
        before = app.state.telemetry.snapshot()
        await c.post("/api/v1/assist", json={"message": "x", "scenario": "retrieval_error"})
        after = app.state.telemetry.snapshot()
        assert window_delta(before, after)["error_rate"] == 1
        assert window_delta(after, after)["error_rate"] is None
        with pytest.raises(ValueError):
            window_delta(after, before)


@pytest.mark.anyio
async def test_bounded_retention_cumulative_aggregate():
    async with lab_client() as (app, c):
        for _ in range(205):
            await c.post("/api/v1/assist", json={"message": ""})
        assert app.state.telemetry.total == 205 and len(app.state.telemetry.logs) == 200
        assert app.state.telemetry.buckets[BUCKETS[-1]] == 205


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_different_instances_refused():
    async with lab_client() as (a, ca):
        before = a.state.telemetry.snapshot()
    async with lab_client() as (b, cb):
        after = b.state.telemetry.snapshot()
    with pytest.raises(ValueError, match="different process"):
        window_delta(before, after)
