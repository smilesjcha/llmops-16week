"""TRACE/01 — a first-day, observable LLM service."""

from __future__ import annotations

import hashlib
import math
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from .providers import PROMPTS, DemoProvider, OllamaProvider, ProviderError
from .schemas import GenerateRequest, GenerateResponse, StatsResponse, TraceRecord
from .telemetry import TraceStore

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
DEFAULT_LOG_PATH = APP_DIR.parent / "data" / "traces.jsonl"


def _estimated_tokens(value: str) -> int:
    """A teaching estimate, not a tokenizer-backed billing value."""
    return 0 if not value else max(1, math.ceil(len(value) / 3))


def _fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def create_app(log_path: Path | None = None) -> FastAPI:
    app = FastAPI(
        title="TRACE/01",
        version="1.0.0",
        description="Week 01: one request, one trace, one improvement loop.",
    )
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.state.trace_store = TraceStore(log_path or DEFAULT_LOG_PATH)
    app.state.providers = {
        "demo": DemoProvider(),
        "ollama": OllamaProvider(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
            model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        ),
    }

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "TRACE/01", "version": app.version}

    @app.post("/api/v1/generate", response_model=GenerateResponse)
    async def generate(request: GenerateRequest) -> GenerateResponse:
        trace_id = uuid4().hex[:12]
        started = time.perf_counter()
        result_text = ""
        model = "unknown"
        status = "ok"
        error_type: str | None = None
        provider = app.state.providers[request.provider]

        try:
            result = await provider.generate(request.text, request.task, request.temperature)
            result_text = result.text
            model = result.model
        except ProviderError as exc:
            status = "error"
            error_type = type(exc).__name__
            latency_ms = round((time.perf_counter() - started) * 1_000, 2)
            trace = TraceRecord(
                trace_id=trace_id,
                created_at=datetime.now(UTC),
                task=request.task,
                provider=request.provider,
                model=model,
                prompt_version=PROMPTS[request.task][0],
                status=status,
                latency_ms=latency_ms,
                input_chars=len(request.text),
                output_chars=0,
                input_tokens_est=_estimated_tokens(request.text),
                output_tokens_est=0,
                content_fingerprint=_fingerprint(request.text),
                error_type=error_type,
            )
            app.state.trace_store.append(trace)
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        latency_ms = round((time.perf_counter() - started) * 1_000, 2)
        trace = TraceRecord(
            trace_id=trace_id,
            created_at=datetime.now(UTC),
            task=request.task,
            provider=request.provider,
            model=model,
            prompt_version=PROMPTS[request.task][0],
            status=status,
            latency_ms=latency_ms,
            input_chars=len(request.text),
            output_chars=len(result_text),
            input_tokens_est=_estimated_tokens(request.text),
            output_tokens_est=_estimated_tokens(result_text),
            content_fingerprint=_fingerprint(request.text),
            error_type=error_type,
        )
        app.state.trace_store.append(trace)
        return GenerateResponse(output=result_text, trace=trace)

    @app.get("/api/v1/traces", response_model=list[TraceRecord])
    async def traces(limit: int = Query(default=20, ge=1, le=100)) -> list[TraceRecord]:
        return app.state.trace_store.latest(limit)

    @app.get("/api/v1/stats", response_model=StatsResponse)
    async def stats() -> StatsResponse:
        return app.state.trace_store.stats()

    @app.get("/metrics", response_class=PlainTextResponse)
    async def metrics() -> str:
        return app.state.trace_store.prometheus_text()

    return app


app = create_app()
