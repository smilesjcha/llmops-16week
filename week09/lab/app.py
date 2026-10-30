"""Local-only API. Start with one worker and bind to 127.0.0.1."""

from dataclasses import replace
import os
from pathlib import Path
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from .service import ChatRequest, ChatResponse, Service, ServiceError, Settings


def create_app(settings: Settings | None = None, *, transport=None) -> FastAPI:
    cfg = settings or Settings()
    service = Service(cfg, transport=transport)
    app = FastAPI(
        title="LLMOps Week 09 API Lab",
        version="0.1.0",
        description="로컬 교육용 MOCK 서비스. 인증·영구 저장·다중 worker 지원 없음.",
    )
    app.state.service = service

    @app.middleware("http")
    async def request_id(request, call_next):
        request.state.request_id = uuid.uuid4().hex
        request.state.started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        return response

    @app.exception_handler(ServiceError)
    async def service_error(request, exc):
        headers = {"Retry-After": "1"} if exc.status in (429, 503) else {}
        return JSONResponse(
            status_code=exc.status,
            headers=headers,
            content={
                "error": {"code": exc.code, "message": exc.message},
                "request_id": request.state.request_id,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        # Default Pydantic errors can include the original input. Omit it.
        service.record(request.state.request_id, 422, request.state.started)
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "입력 필드·길이·형식을 확인하세요.",
                    "fields": [
                        {"location": list(e["loc"]), "type": e["type"]} for e in exc.errors()
                    ],
                },
                "request_id": request.state.request_id,
            },
        )

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def index():
        return Path(__file__).with_name("index.html").read_text(encoding="utf-8")

    @app.get("/health")
    async def health():
        return {"status": "alive", "provider": cfg.provider}

    @app.get("/ready")
    async def ready():
        if cfg.provider == "mock":
            return {"ready": True, "provider": "mock", "simulated": True}
        # Deliberately no hidden model download or generation on readiness probe.
        import httpx

        try:
            async with httpx.AsyncClient(
                base_url=cfg.ollama_url, timeout=2, transport=transport, trust_env=False
            ) as client:
                r = await client.get("/api/tags")
                r.raise_for_status()
                names = {m["name"] for m in r.json()["models"]}
                if cfg.model not in names:
                    raise ValueError("model missing")
        except (httpx.HTTPError, ValueError, KeyError, TypeError):
            raise ServiceError(503, "not_ready", "Ollama 서버와 설치 모델명을 확인하세요.")
        return {
            "ready": True,
            "provider": "ollama",
            "model": cfg.model,
            "note": "설치 확인만 수행. 실제 생성 성공은 별도 확인.",
        }

    @app.post(
        "/api/v1/chat",
        response_model=ChatResponse,
        responses={
            422: {"description": "입력 오류"},
            429: {"description": "빈도 제한"},
            502: {"description": "상류 오류"},
            503: {"description": "용량·연결 오류"},
            504: {"description": "처리 제한시간 초과"},
        },
    )
    async def chat(body: ChatRequest, request: Request):
        return await service.chat(body, request.state.request_id)

    @app.post("/api/v1/chat/stream", response_class=StreamingResponse)
    async def stream(body: ChatRequest, request: Request):
        if cfg.provider != "mock":
            raise ServiceError(409, "mock_stream_only", "이번 스트리밍 실습은 MOCK 전용입니다.")
        try:
            service.admit()
        except ServiceError as exc:
            service.record(request.state.request_id, exc.status, request.state.started)
            raise
        return StreamingResponse(
            service.stream(body, request.state.request_id, request),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    @app.get("/lab/stats")
    async def stats():
        return {
            "active": service.active,
            "provider_calls": service.provider_calls,
            "cache_entries": len(service.cache.values),
            "traces": list(service.traces),
            "scope": "single process, last 200 traces; no prompt or answer logs",
        }

    return app


def environment_settings():
    provider = os.getenv("WEEK09_PROVIDER", "mock")
    cfg = Settings()
    if provider == "ollama":
        model = os.getenv("WEEK09_MODEL", "").strip()
        if not model:
            raise ValueError("WEEK09_MODEL must match an installed model from ollama list")
        return replace(cfg, provider=provider, model=model, timeout_s=30)
    if provider != "mock":
        raise ValueError("WEEK09_PROVIDER must be mock or ollama")
    return cfg


app = create_app(environment_settings())
