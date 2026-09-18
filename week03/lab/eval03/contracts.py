"""Bounded request models for the Week 03 evaluation lab."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

PromptVersion = Literal["v0.1", "v0.2"]
Split = Literal["dev", "test"]


class EvaluationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    split: Split = "dev"
    versions: list[PromptVersion] = Field(
        default_factory=lambda: ["v0.1", "v0.2"], min_length=1, max_length=2
    )

    @field_validator("versions")
    @classmethod
    def reject_duplicates(cls, values):
        if len(values) != len(set(values)):
            raise ValueError("같은 버전은 한 번만 선택할 수 있습니다.")
        return values


class DecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    run_id: str = Field(min_length=1, max_length=80)
    version: PromptVersion
    decision: Literal["hold", "candidate", "reject"]
    reason: str = Field(min_length=20, max_length=1000)
