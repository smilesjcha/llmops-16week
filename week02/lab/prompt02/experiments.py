"""Comparable runs, process-local history and non-deployment decision records."""

from __future__ import annotations

import asyncio
import time
from datetime import UTC, datetime
from uuid import uuid4

from .contracts import ExperimentRequest
from .core import (
    EVALUATOR_VERSION,
    aggregate,
    fingerprint,
    load_dataset,
    load_prompt,
    render_prompt,
    validate_output,
)
from .providers import DemoProvider, OllamaProvider, ProviderError


async def run_experiment(request: ExperimentRequest, provider_override=None) -> dict:
    dataset = load_dataset()
    by_id = {case["id"]: case for case in dataset["cases"]}
    ids = request.case_ids or list(by_id)
    if any(case_id not in by_id for case_id in ids):
        raise ValueError("데이터 세트에 없는 case_id가 포함되어 있습니다.")
    cases = [by_id[case_id] for case_id in ids]
    provider = provider_override or (
        DemoProvider() if request.provider == "demo" else OllamaProvider()
    )
    config = provider.config()
    # Snapshot all templates once, so edits during a run cannot mix versions silently.
    templates = {version: load_prompt(version) for version in request.versions}
    prompts = {
        (version, case["id"]): render_prompt(version, case, template=templates[version])
        for version in request.versions
        for case in cases
    }
    rows, stopped = [], None
    started = time.perf_counter()
    for case in cases:
        for version in request.versions:
            prompt = prompts[version, case["id"]]
            tick = time.perf_counter()
            error, output, metadata = stopped, "", {}
            if not stopped:
                try:
                    remaining = 120 - (tick - started)
                    if remaining <= 0:
                        raise TimeoutError
                    metadata = await asyncio.wait_for(
                        provider.generate(prompt, case), timeout=min(35, remaining)
                    )
                    output = metadata.pop("text")
                except (ProviderError, TimeoutError) as exc:
                    error = str(exc) or "실험 시간 상한을 초과했습니다."
                    stopped = f"앞선 호출 오류로 미실행: {error}"
            validation = (
                validate_output(output, case)
                if error is None
                else {
                    "format_ok": None,
                    "routing_ok": None,
                    "promise_ok": None,
                    "review_ok": None,
                    "overall_ok": False,
                    "parsed": None,
                    "issues": [error],
                }
            )
            rows.append(
                {
                    "case_id": case["id"],
                    "tag": case["tag"],
                    "version": version,
                    "input": case["text"],
                    "input_hash": prompt["input_hash"],
                    "prompt_hash": prompt["prompt_hash"],
                    "rendered_prompt_hash": prompt["rendered_prompt_hash"],
                    "raw_output": output,
                    "validation": validation,
                    "error": error,
                    "latency_ms": round((time.perf_counter() - tick) * 1000, 3),
                    "model_metadata": metadata,
                    "expected": {
                        "category": case["expected_category"],
                        "priority": case["expected_priority"],
                        "needs_review": case["expected_review"],
                        "rationale": case["rationale"],
                    },
                }
            )
    return {
        "run_id": f"run-{uuid4().hex[:12]}",
        "created_at": datetime.now(UTC).isoformat(),
        "provider": request.provider,
        "simulation": config["simulation"],
        "config": config,
        "dataset_id": dataset["dataset_id"],
        "dataset_hash": fingerprint(dataset),
        "input_set_hash": fingerprint(cases),
        "evaluator_version": EVALUATOR_VERSION,
        "versions": request.versions,
        "case_ids": ids,
        "prompt_snapshots": templates,
        "rows": rows,
        "summary": aggregate(rows, request.versions),
        "decisions": [],
        "limitations": [
            "합성 문의 8건은 운영 성능의 증거가 아닙니다.",
            "확정 약속 검사는 제한된 정규표현식이며 우회 표현을 모두 탐지하지 못합니다.",
            "JSON 형식 통과는 의미 정확성과 별도입니다. 형식 실패 시 의미 검사는 미평가입니다.",
            "버전·데이터·모델 설정을 함께 기록해도 "
            "하드웨어·모델 파일 차이로 결과가 달라질 수 있습니다.",
        ],
    }
