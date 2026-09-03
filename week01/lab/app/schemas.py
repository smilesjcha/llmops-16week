"""Public request, response, and trace contracts for TRACE/01."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TaskName = Literal["summarize", "extract", "rewrite"]
ProviderName = Literal["demo", "ollama"]


class GenerateRequest(BaseModel):
    """A deliberately small generation contract for the first lab."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    text: str = Field(min_length=2, max_length=6_000)
    task: TaskName = "summarize"
    provider: ProviderName = "demo"
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)


class TraceRecord(BaseModel):
    """Metadata required to compare two LLM runs without storing raw content."""

    trace_id: str
    created_at: datetime
    task: TaskName
    provider: ProviderName
    model: str
    prompt_version: str
    status: Literal["ok", "error"]
    latency_ms: float = Field(ge=0)
    input_chars: int = Field(ge=0)
    output_chars: int = Field(ge=0)
    input_tokens_est: int = Field(ge=0)
    output_tokens_est: int = Field(ge=0)
    content_fingerprint: str
    error_type: str | None = None


class GenerateResponse(BaseModel):
    output: str
    trace: TraceRecord


class StatsResponse(BaseModel):
    total_requests: int
    success_rate: float
    average_latency_ms: float
    p95_latency_ms: float
    estimated_tokens: int
    providers: dict[str, int]
