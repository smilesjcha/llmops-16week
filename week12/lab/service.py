"""Local-only experiment service: stable allocation, idempotency and real event storage."""
from datetime import datetime, timezone, timedelta
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sqlite3
import time
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel, Field, ConfigDict
import pandas as pd

from .analysis import analyze
from .experiment import DEFAULT, assign, template_answer
from .ollama import generate


def now():
    return datetime.now(timezone.utc).isoformat()


class AnswerInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    visitor_id: str = Field(pattern=r"^u-[a-zA-Z0-9_-]{1,48}$")
    request_id: str = Field(pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    topic: Literal["exchange", "return", "stock"] = "exchange"
    provider: Literal["template", "ollama"] = "template"


class Feedback(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str
    resolved: bool


class Control(BaseModel):
    enabled: bool


def create_app(db_path=None, *, config=DEFAULT, generator=generate):
    app = FastAPI(title="W12 · 온라인 실험 실습", version="1.0")
    default_db = Path(__file__).resolve().parent / "reports/events.sqlite3"
    db_path = Path(db_path or os.getenv("W12_DB", str(default_db)))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    app.state.experiment_enabled = True

    @contextmanager
    def connection():
        con = sqlite3.connect(db_path, timeout=20)
        con.row_factory = sqlite3.Row
        try:
            with con:
                yield con
        finally:
            con.close()

    with connection() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS requests (
            request_id TEXT PRIMARY KEY, visitor_id TEXT NOT NULL, assigned_variant TEXT NOT NULL,
            served_variant TEXT NOT NULL, config_version TEXT NOT NULL, experiment_id TEXT NOT NULL,
            topic TEXT NOT NULL, provider TEXT NOT NULL, entered_at TEXT NOT NULL,
            status TEXT NOT NULL, response_json TEXT, latency_ms REAL, resolved INTEGER, feedback_at TEXT)""")

    @app.get("/", response_class=HTMLResponse)
    def home():
        return Path(__file__).with_name("app.html").read_text()

    @app.get("/health")
    def health():
        return {"status": "ok", "experiment_id": config.experiment_id, "config_version": config.version,
                "enabled": app.state.experiment_enabled, "data": "local teaching requests"}

    @app.post("/api/answer")
    def answer(payload: AnswerInput):
        assigned = assign(payload.visitor_id, config)
        enabled_at_entry = app.state.experiment_enabled
        served = assigned if enabled_at_entry else "A"
        with connection() as con:
            old = con.execute("SELECT * FROM requests WHERE request_id=?", (payload.request_id,)).fetchone()
            if old:
                if (old["visitor_id"], old["topic"], old["provider"]) != (payload.visitor_id, payload.topic, payload.provider):
                    raise HTTPException(409, "같은 request_id를 다른 요청에 재사용할 수 없습니다.")
                if old["status"] == "pending":
                    raise HTTPException(409, "처리 중입니다. 완료 후 같은 ID로 재시도하세요.")
                data = json.loads(old["response_json"])
                if old["status"] == "error":
                    raise HTTPException(503, data)
                return {**data, "replayed": True}
            try:
                con.execute("INSERT INTO requests VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                    payload.request_id, payload.visitor_id, assigned, served, config.version,
                    config.experiment_id, payload.topic, payload.provider, now(), "pending", None, None, None, None))
            except sqlite3.IntegrityError as exc:
                raise HTTPException(409, "동일 ID 요청 처리 중. 같은 ID로 다시 확인하세요.") from exc
        started = time.perf_counter()
        result = {"request_id": payload.request_id, "visitor_id": payload.visitor_id,
                  "assigned_variant": assigned, "variant": served, "config_version": config.version,
                  "experiment_enabled": enabled_at_entry}
        status = "ok"
        try:
            generated = generator(payload.topic, served) if payload.provider == "ollama" else {
                "answer": template_answer(payload.topic, served), "provider": "template", "model": None, "output_tokens": 0}
            result.update(generated)
        except (RuntimeError, ValueError) as exc:
            status = "error"
            result.update(error=str(exc), provider=payload.provider)
        result["latency_ms"] = round((time.perf_counter()-started)*1000, 2)
        with connection() as con:
            con.execute("UPDATE requests SET status=?,response_json=?,latency_ms=? WHERE request_id=?",
                        (status, json.dumps(result, ensure_ascii=False), result["latency_ms"], payload.request_id))
        if status == "error":
            raise HTTPException(503, result)
        return {**result, "replayed": False}

    @app.post("/api/feedback")
    def feedback(payload: Feedback):
        with connection() as con:
            row = con.execute("SELECT * FROM requests WHERE request_id=?", (payload.request_id,)).fetchone()
            if not row:
                raise HTTPException(404, "요청을 먼저 실행하세요.")
            if row["status"] != "ok":
                raise HTTPException(409, "성공 응답이 없는 요청에는 피드백을 붙일 수 없습니다.")
            if row["resolved"] is not None and row["resolved"] != int(payload.resolved):
                raise HTTPException(409, "이미 제출된 피드백입니다. 같은 값 재전송만 허용합니다.")
            if datetime.now(timezone.utc)-datetime.fromisoformat(row["entered_at"]) > timedelta(minutes=config.observation_minutes):
                raise HTTPException(409, "30분 관찰 창이 지났습니다. 새 요청으로 실습하세요.")
            con.execute("UPDATE requests SET resolved=?,feedback_at=COALESCE(feedback_at,?) WHERE request_id=?",
                        (int(payload.resolved), now(), payload.request_id))
        return {"stored": True, "request_id": payload.request_id, "resolved": payload.resolved}

    @app.get("/api/events")
    def events():
        with connection() as con:
            records = con.execute("SELECT * FROM requests ORDER BY entered_at,request_id").fetchall()
        return [dict(r) for r in records]

    @app.get("/api/summary")
    def summary():
        records = events()
        if not records:
            return {"decision": "WAIT", "reasons": ["먼저 요청을 보내세요."], "users": 0}
        # The first eligible request, selected before examining its outcome.
        first = {}
        for r in records:
            first.setdefault(r["visitor_id"], r)
        if any(r["status"] == "pending" for r in first.values()):
            return {"decision": "WAIT", "reasons": ["처리 중인 요청이 있습니다."], "users": len(first)}
        if any(r["assigned_variant"] != r["served_variant"] or not json.loads(r["response_json"] or "{}").get("experiment_enabled", True) for r in records):
            return {"decision": "INVALID", "reasons": ["중단 스위치로 실제 제공 버전이 변경됨. 변경 전후를 합치지 마세요."], "users": len(first)}
        providers = {r["provider"] for r in first.values()}
        if len(providers) > 1:
            return {"decision": "INVALID", "reasons": ["템플릿과 실제 모델 요청이 섞였습니다. 별도 DB로 실험하세요."], "users": len(first)}
        rows = [{"visitor_id": r["visitor_id"], "variant": r["assigned_variant"], "config_version": r["config_version"],
                 "experiment_id": r["experiment_id"], "resolved": r["resolved"] or 0,
                 "feedback_received": int(r["resolved"] is not None), "exposed": int(r["status"] == "ok"),
                 "error": int(r["status"] == "error"), "latency_ms": r["latency_ms"], "source": "local_service"} for r in first.values()]
        report = analyze(pd.DataFrame(rows), config, elapsed_days=0, outcomes_mature=False)
        report["users"] = len(first)
        report["note"] = "응답 성공을 노출의 서버 대리 지표로 사용. 실제 서비스는 클라이언트 렌더 이벤트도 필요. 교실 요청으로 사업 효과를 판정하지 않음."
        return report

    @app.post("/api/control")
    def control(payload: Control):
        app.state.experiment_enabled = payload.enabled
        return {"enabled": payload.enabled, "note": "비활성화하면 새 요청은 A. 기존 요청 ID의 재시도는 원래 응답 유지."}

    @app.get("/metrics", response_class=PlainTextResponse)
    def metrics():
        rows = events()
        lines = ["# HELP w12_requests_total Recorded local requests, including failures.", "# TYPE w12_requests_total counter"]
        for variant in ["A", "B"]:
            count = sum(r["served_variant"] == variant for r in rows)
            lines.append(f'w12_requests_total{{variant="{variant}"}} {count}')
        # Pending decreases when a request completes: this is a gauge, not a counter.
        lines += ["# HELP w12_requests_by_status Current recorded requests by processing state.",
                  "# TYPE w12_requests_by_status gauge"]
        for variant in ["A", "B"]:
            for status in ["ok", "error", "pending"]:
                count = sum(r["served_variant"] == variant and r["status"] == status for r in rows)
                lines.append(f'w12_requests_by_status{{variant="{variant}",status="{status}"}} {count}')
        lines += ["# TYPE w12_unique_users gauge", f"w12_unique_users {len({r['visitor_id'] for r in rows})}"]
        return "\n".join(lines)+"\n"

    return app


app = create_app()
