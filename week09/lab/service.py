"""Single-process teaching service. No authentication or production guarantees.

The default provider is a deterministic simulator, not an LLM. All state is
bounded and in memory. Never send personal data; a hash is not encryption.
"""

from __future__ import annotations

import asyncio
from collections import OrderedDict, deque
from dataclasses import dataclass
import hashlib
import json
import math
import time
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field, field_validator

PROMPTS = {
    "v1": "수업용 합성 사례의 안내 도우미입니다. 확인되지 않은 정책을 단정하지 말고 검토가 필요한 부분을 표시하세요.",
    "v2": "수업용 합성 사례의 안내 도우미입니다. 요점과 다음 행동을 짧게 제시하고 근거가 없으면 검토를 요청하세요.",
}


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    message: str = Field(min_length=1, max_length=1000)
    max_tokens: int = Field(default=64, ge=8, le=128)
    use_cache: bool = True
    scenario: Literal["normal", "timeout", "upstream_error"] = "normal"

    @field_validator("message")
    @classmethod
    def nonblank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("nonblank message required")
        return value


class ChatResponse(BaseModel):
    request_id: str
    output: str
    provider: str
    model: str
    prompt_version: str
    cached: bool
    elapsed_ms: float
    simulated: bool


@dataclass(frozen=True)
class Settings:
    provider: str = "mock"
    model: str = "teaching-mock-v1"
    prompt_version: str = "v1"
    max_inflight: int = 2
    timeout_s: float = 0.3
    mock_delay_s: float = 0.04
    cache_ttl_s: float = 30.0
    cache_entries: int = 128
    rate_per_s: float = 100.0
    burst: int = 100
    ollama_url: str = "http://127.0.0.1:11434"

    def __post_init__(self):
        if self.provider not in ("mock", "ollama"):
            raise ValueError("provider must be mock or ollama")
        for name in ("timeout_s", "cache_ttl_s", "rate_per_s"):
            if not math.isfinite(getattr(self, name)) or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be finite and positive")
        if not math.isfinite(self.mock_delay_s) or self.mock_delay_s < 0:
            raise ValueError("mock_delay_s must be finite and nonnegative")
        if any(
            type(value) is not int or value < 1
            for value in (self.max_inflight, self.cache_entries, self.burst)
        ):
            raise ValueError("capacities must be positive")
        if not self.model.strip() or not self.prompt_version.strip():
            raise ValueError("model and prompt version required")
        if self.prompt_version not in PROMPTS:
            raise ValueError("unknown server-owned prompt version")


class ServiceError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message
        super().__init__(code)


class TTLCache:
    def __init__(self, ttl: float, capacity: int, clock=time.monotonic):
        self.ttl, self.capacity, self.clock = ttl, capacity, clock
        self.values: OrderedDict[str, tuple[str, float]] = OrderedDict()

    def get(self, key: str) -> str | None:
        item = self.values.get(key)
        if item is None:
            return None
        if self.clock() >= item[1]:
            del self.values[key]
            return None
        self.values.move_to_end(key)
        return item[0]

    def set(self, key: str, value: str):
        self.values[key] = (value, self.clock() + self.ttl)
        self.values.move_to_end(key)
        while len(self.values) > self.capacity:
            self.values.popitem(last=False)


class TokenBucket:
    """One global process-local bucket, not a per-user security boundary."""

    def __init__(self, rate: float, burst: int, clock=time.monotonic):
        self.rate, self.burst, self.clock = rate, burst, clock
        self.tokens, self.last = float(burst), clock()

    def allow(self) -> bool:
        now = self.clock()
        self.tokens = min(self.burst, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens < 1:
            return False
        self.tokens -= 1
        return True


def cache_key(req: ChatRequest, settings: Settings) -> str:
    # Server-owned versions. A real multi-tenant service must also bind identity,
    # document permissions, source revisions and all generation parameters.
    payload = {
        "message": req.message,
        "max_tokens": req.max_tokens,
        "provider": settings.provider,
        "model": settings.model,
        "prompt_version": settings.prompt_version,
        "schema": "v1",
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def mock_answer(message: str) -> str:
    if "반품" in message:
        return "[합성 정책 예시] 반품 조건과 적용 날짜를 확인하고, 근거가 없으면 담당자 검토를 요청합니다."
    return (
        "[MOCK] 요청을 확인했습니다. 대상 사용자, 기대 출력, 실패 시 다음 행동을 함께 정의하세요."
    )


class Service:
    def __init__(self, settings: Settings, transport=None):
        self.settings, self.transport = settings, transport
        self.cache = TTLCache(settings.cache_ttl_s, settings.cache_entries)
        self.bucket = TokenBucket(settings.rate_per_s, settings.burst)
        self.active, self.provider_calls = 0, 0
        self.traces: deque[dict] = deque(maxlen=200)

    def admit(self):
        # No await between check and increment: atomic on one asyncio event loop.
        if not self.bucket.allow():
            raise ServiceError(429, "rate_limited", "요청 빈도 제한입니다. 잠시 후 재시도하세요.")
        if self.active >= self.settings.max_inflight:
            raise ServiceError(
                503, "capacity_exceeded", "동시 처리 한도입니다. 요청 수를 줄이세요."
            )
        self.active += 1

    def record(self, request_id, status, started, cached=False, **extra):
        # No message, answer, identity, token or provider error body is logged.
        self.traces.append(
            {
                "request_id": request_id,
                "status": status,
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
                "cached": cached,
                "provider": self.settings.provider,
                **extra,
            }
        )

    async def generate(self, req: ChatRequest) -> str:
        self.provider_calls += 1
        cfg = self.settings
        if cfg.provider == "mock":
            if req.scenario == "upstream_error":
                raise ServiceError(502, "upstream_error", "모델 연결 응답 오류입니다.")
            delay = cfg.timeout_s * 2 if req.scenario == "timeout" else cfg.mock_delay_s
            await asyncio.sleep(delay)
            return mock_answer(req.message)
        if req.scenario != "normal":
            raise ServiceError(409, "mock_only_scenario", "장애 주입은 MOCK 모드 전용입니다.")
        try:
            async with httpx.AsyncClient(
                base_url=cfg.ollama_url,
                timeout=cfg.timeout_s,
                transport=self.transport,
                trust_env=False,
            ) as client:
                response = await client.post(
                    "/api/chat",
                    json={
                        "model": cfg.model,
                        "messages": [
                            {"role": "system", "content": PROMPTS[cfg.prompt_version]},
                            {"role": "user", "content": req.message},
                        ],
                        "stream": False,
                        "think": False,
                        "options": {"num_predict": req.max_tokens, "temperature": 0},
                    },
                )
                response.raise_for_status()
                value = response.json()["message"]["content"]
                if not isinstance(value, str) or not value.strip():
                    raise ValueError("empty provider answer")
                return value
        except httpx.TimeoutException as exc:
            raise ServiceError(504, "provider_timeout", "모델 응답 대기시간 초과입니다.") from exc
        except httpx.ConnectError as exc:
            raise ServiceError(
                503, "provider_unavailable", "Ollama 실행과 포트를 확인하세요."
            ) from exc
        except httpx.HTTPStatusError as exc:
            code = "model_not_found" if exc.response.status_code == 404 else "upstream_error"
            raise ServiceError(502, code, "Ollama 모델명·설치·서버 버전을 확인하세요.") from exc
        except (httpx.RequestError, ValueError, KeyError, TypeError) as exc:
            raise ServiceError(502, "invalid_upstream", "모델 응답 형식 오류입니다.") from exc

    async def chat(self, req: ChatRequest, request_id: str) -> ChatResponse:
        started = time.perf_counter()
        try:
            self.admit()
        except ServiceError as exc:
            self.record(request_id, exc.status, started)
            raise
        try:
            key = cache_key(req, self.settings)
            # Fault injection bypasses cached success so it remains observable.
            use_cache = req.use_cache and req.scenario == "normal"
            output = self.cache.get(key) if use_cache else None
            hit = output is not None
            if output is None:
                try:
                    async with asyncio.timeout(self.settings.timeout_s):
                        output = await self.generate(req)
                except TimeoutError as exc:
                    raise ServiceError(
                        504, "deadline_exceeded", "처리 제한시간 초과입니다."
                    ) from exc
                if use_cache:
                    self.cache.set(key, output)
            result = ChatResponse(
                request_id=request_id,
                output=output,
                provider=self.settings.provider,
                model=self.settings.model,
                prompt_version=self.settings.prompt_version,
                cached=hit,
                elapsed_ms=round((time.perf_counter() - started) * 1000, 3),
                simulated=self.settings.provider == "mock",
            )
            self.record(request_id, 200, started, hit)
            return result
        except ServiceError as exc:
            self.record(request_id, exc.status, started)
            raise
        except asyncio.CancelledError:
            self.record(request_id, "cancelled", started)
            raise
        finally:
            self.active -= 1

    async def stream(self, req: ChatRequest, request_id: str, request):
        """Caller admitted before headers; generator owns release afterwards."""
        started, first_delta, status = time.perf_counter(), None, "stream_complete"

        def event(name, data):
            return f"event: {name}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

        try:
            yield event("meta", {"request_id": request_id, "simulated": True})
            try:
                async with asyncio.timeout(self.settings.timeout_s):
                    self.provider_calls += 1
                    if req.scenario == "upstream_error":
                        raise ServiceError(502, "upstream_error", "주입한 상류 오류")
                    if req.scenario == "timeout":
                        await asyncio.sleep(self.settings.timeout_s * 2)
                    # Chunks are character groups of a fixed answer, NOT LLM tokens.
                    answer = mock_answer(req.message)
                    for offset in range(0, len(answer), 12):
                        await asyncio.sleep(self.settings.mock_delay_s)
                        if await request.is_disconnected():
                            status = "disconnected"
                            return
                        if first_delta is None:
                            first_delta = round((time.perf_counter() - started) * 1000, 3)
                        yield event("delta", {"text": answer[offset : offset + 12]})
                    yield event("done", {"request_id": request_id, "complete": True})
            except (TimeoutError, ServiceError) as exc:
                status = "stream_error"
                code = exc.code if isinstance(exc, ServiceError) else "deadline_exceeded"
                yield event("error", {"code": code, "request_id": request_id, "complete": False})
        except asyncio.CancelledError:
            status = "cancelled"
            raise
        finally:
            self.active -= 1
            self.record(request_id, status, started, first_delta_ms=first_delta)
