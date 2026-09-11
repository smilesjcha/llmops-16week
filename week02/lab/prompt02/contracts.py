"""Strict output contract and bounded API requests."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Version = Literal["v1", "v2", "v3"]
Category = Literal["delivery", "refund", "exchange", "account", "other"]


class TicketResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)

    category: Category
    priority: Literal["normal", "urgent"]
    needs_review: bool
    reply: str = Field(min_length=5, max_length=160)


class ExperimentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: Literal["demo", "ollama"] = "demo"
    versions: list[Version] = Field(default_factory=lambda: ["v1", "v2", "v3"], min_length=1)
    case_ids: list[str] | None = Field(default=None, min_length=1, max_length=8)

    @field_validator("versions", "case_ids")
    @classmethod
    def reject_duplicates(cls, values):
        if values is not None and len(values) != len(set(values)):
            raise ValueError("중복된 항목은 비교에 사용할 수 없습니다.")
        return values


class DecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    run_id: str = Field(min_length=1, max_length=80)
    version: Version
    reason: str = Field(min_length=15, max_length=1000)
