"""Deterministic run builder for a comparable offline evaluation lesson."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from .contracts import EvaluationRequest
from .core import (
    EVALUATOR_VERSION,
    aggregate,
    cases_for_split,
    evaluate,
    fingerprint,
    load_demo_outputs,
    load_prompt,
)


def run_evaluation(request: EvaluationRequest) -> dict:
    cases = cases_for_split(request.split)
    outputs = load_demo_outputs()
    templates = {version: load_prompt(version) for version in request.versions}
    rows = []
    for case in cases:
        for version in request.versions:
            raw = outputs[case["id"]][version]
            rows.append(
                {
                    "case_id": case["id"],
                    "split": case["split"],
                    "tag": case["tag"],
                    "version": version,
                    "input": case["transcript"],
                    "input_hash": fingerprint({"id": case["id"], "transcript": case["transcript"]}),
                    "prompt_hash": fingerprint(templates[version]),
                    "raw_output": raw,
                    "expected": case["expected"],
                    "evaluation": evaluate(raw, case),
                }
            )
    dataset = {"split": request.split, "cases": cases}
    return {
        "run_id": f"eval-{uuid4().hex[:12]}",
        "created_at": datetime.now(UTC).isoformat(),
        "provider": "fixed-teaching-fixtures-v1",
        "simulation": True,
        "split": request.split,
        "versions": request.versions,
        "prompt_snapshots": templates,
        "dataset_hash": fingerprint(dataset),
        "evaluator_version": EVALUATOR_VERSION,
        "rows": rows,
        "summary": aggregate(rows, request.versions),
        "decisions": [],
        "limitations": [
            "고정 응답은 실제 모델 성능 측정이 아닙니다.",
            "이 평가기는 제공된 합성 회의록의 제한된 섹션·문구만 확인합니다.",
            "실제 회의록 평가에는 원문 근거 검토와 사람의 판단이 추가로 필요합니다.",
            "dev 통과 결과는 별도 test 사례에서 다시 확인해야 합니다.",
        ],
    }
