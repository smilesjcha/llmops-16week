"""Run: python -m uvicorn week10.lab.app:app --host 127.0.0.1 --port 8010."""

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
import secrets
import time
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import Settings
from .telemetry import ORIGIN, PARENT, TRACE, Telemetry, trace_context


class AssistRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    message: str = Field(min_length=1, max_length=600)
    scenario: Literal["normal", "slow", "retrieval_error", "provider_error"] = "normal"

    @field_validator("message")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("blank")
        return value


class AssistResponse(BaseModel):
    request_id: str
    trace_id: str
    release: str
    answer: str
    simulated: bool = True


class ServiceError(Exception):
    def __init__(self, status, code):
        self.status, self.code = status, code


def create_app(settings=None):
    cfg = settings or Settings.from_env()
    obs = Telemetry(cfg.manifest(), emit_logs=cfg.emit_logs)

    @asynccontextmanager
    async def lifespan(app):
        app.state.started = True
        try:
            yield
        finally:
            app.state.draining = True
            app.state.started = False

    app = FastAPI(title="LLMOps Week 10 · Release & Observe", version="1.0", lifespan=lifespan)
    app.state.telemetry = obs
    app.state.started = False
    app.state.draining = False
    app.state.dependency_ok = True  # Notebook/test fixture only; no remote control endpoint.

    @app.middleware("http")
    async def observe(request, call_next):
        if request.url.path != "/api/v1/assist":
            return await call_next(request)
        tid, parent = trace_context(request.headers.get("traceparent"))
        rid = secrets.token_hex(12)
        request.state.request_id, request.state.trace_id = rid, tid
        started = time.perf_counter()
        tokens = [TRACE.set(tid), PARENT.set(parent), ORIGIN.set(started)]
        status = 499  # Internal cancellation marker; not a response sent to the client.
        try:
            response = await call_next(request)
            status = response.status_code
            response.headers["X-Request-ID"] = rid
            response.headers["X-Trace-ID"] = tid
            response.headers["X-Release"] = cfg.release
            return response
        except Exception:
            status = 500
            return JSONResponse(
                status_code=500,
                content={"error": "internal_error", "request_id": rid},
                headers={"X-Request-ID": rid, "X-Trace-ID": tid, "X-Release": cfg.release},
            )
        finally:
            obs.finish(request_id=rid, status=status, started=started)
            ORIGIN.reset(tokens[2])
            PARENT.reset(tokens[1])
            TRACE.reset(tokens[0])

    @app.exception_handler(RequestValidationError)
    async def invalid(request, exc):
        return JSONResponse(
            status_code=422,
            content={"error": "invalid_input", "request_id": request.state.request_id},
        )

    @app.exception_handler(ServiceError)
    async def error(request, exc):
        return JSONResponse(
            status_code=exc.status,
            content={"error": exc.code, "request_id": request.state.request_id},
        )

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def index():
        return Path(__file__).with_name("index.html").read_text(encoding="utf-8")

    @app.get("/health/live")
    async def live():
        return {"alive": True, "release": cfg.release}

    @app.get("/health/ready")
    async def ready():
        ok = app.state.started and not app.state.draining and app.state.dependency_ok
        return JSONResponse(
            status_code=200 if ok else 503,
            content={"ready": ok, "release": cfg.release, "simulated": True},
        )

    @app.get("/release")
    async def release():
        return cfg.manifest()

    @app.post("/api/v1/assist", response_model=AssistResponse)
    async def assist(body: AssistRequest, request: Request):
        with obs.span("assist"):
            if not app.state.started or app.state.draining or not app.state.dependency_ok:
                raise ServiceError(503, "not_ready")
            if obs.active >= cfg.capacity:
                raise ServiceError(503, "capacity_exceeded")
            obs.active += 1
            try:
                async with asyncio.timeout(cfg.timeout_s):
                    with obs.span("retrieve"):
                        await asyncio.sleep(0.01)
                        if body.scenario == "retrieval_error":
                            raise ServiceError(502, "retrieval_failed")
                    with obs.span("generate"):
                        await asyncio.sleep(
                            cfg.timeout_s + 0.1 if body.scenario == "slow" else 0.03
                        )
                        if body.scenario == "provider_error":
                            raise ServiceError(502, "provider_failed")
                        answer = (
                            "문서 D01: 신청 후 담당자 확인이 필요합니다."
                            if cfg.release == "v1"
                            else "확인 없이 무조건 승인됩니다."
                        )
                    with obs.span("format"):
                        result = AssistResponse(
                            request_id=request.state.request_id,
                            trace_id=request.state.trace_id,
                            release=cfg.release,
                            answer=answer,
                        )
                    return result
            except TimeoutError:
                raise ServiceError(504, "deadline_exceeded") from None
            finally:
                obs.active -= 1

    @app.get("/lab/snapshot")
    async def snapshot():
        return obs.snapshot()

    @app.get("/metrics", response_class=PlainTextResponse)
    async def metrics():
        return PlainTextResponse(obs.prometheus(), media_type="text/plain; version=0.0.4")

    return app


app = create_app()
