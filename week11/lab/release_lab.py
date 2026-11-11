"""Same-data Langfuse experiments and a fail-closed classroom release gate.

This is a tiny synthetic regression suite, not a service accuracy benchmark.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import uuid
from pathlib import Path

from langfuse import Evaluation

from .evaluation import load_data
from .langfuse_lab import connect_langfuse, traced_question, wait_for_trace
from .ollama_lab import PROMPTS, OllamaClient, inspect_answer

CASE_IDS = ("Q01a", "Q03a", "Q05b", "Q24a")
DEFAULT_POLICY = {
    "max_generation_ms": 3000,
    "max_false_accepts": 0,
    "min_structural_pass_rate": 1.0,
    "human_review_required": True,
}


def regression_cases():
    by_id = {q["id"]: q for q in load_data()[1]}
    # Application input: a UI menu/route, not an answerability label or model inference.
    return [
        {**by_id[key], "requested_capability": "live_inventory" if key == "Q24a" else "policy_qa"}
        for key in CASE_IDS
    ]


def capability_response(requested_capability):
    """Only 'policy_qa' is wired to this service. No reference answers are consulted."""
    if requested_capability == "policy_qa":
        return None
    if requested_capability != "live_inventory":
        raise ValueError("지원하는 요청 유형은 policy_qa와 live_inventory입니다.")
    return {
        "answer": "실시간 조회 기능이 연결되지 않아 현재 재고를 확인할 수 없습니다. 상품 상세 페이지에서 확인해 주세요.",
        "citations": [],
        "abstain": True,
    }


def guarded_question(langfuse, ollama, question):
    answer = capability_response(question["requested_capability"])
    if answer is None:
        return traced_question(langfuse, ollama, question, prompt_version="grounded")
    # A real policy short-circuit, explicitly not an LLM-generated answer or a mock.
    with langfuse.start_as_current_observation(
        name="capability-policy-response",
        input={
            "question": question["query"],
            "requested_capability": question["requested_capability"],
        },
        metadata={
            "response_source": "service-policy",
            "llm_called": False,
            "policy_version": "capabilities-v1",
        },
    ) as root:
        with langfuse.start_as_current_observation(
            name="capability-check", as_type="guardrail"
        ) as guard:
            guard.update(
                input={"available": ["policy_qa"], "requested": question["requested_capability"]},
                output="unsupported capability",
            )
        with langfuse.start_as_current_observation(
            name="contract-checks", as_type="evaluator"
        ) as evaluator:
            checks = inspect_answer(answer, [], question["gold_ids"], question["answerable"])
            evaluator.update(output=checks)
        names = []
        for name, value in checks.items():
            if value is not None:
                names.append(name)
                langfuse.create_score(
                    trace_id=root.trace_id,
                    name=name,
                    value=float(value),
                    data_type="BOOLEAN",
                    comment="코드 검사 / 서비스 정책 응답 / 모델 판정 아님",
                )
        root.update(output=answer)
        trace_id = root.trace_id
    langfuse.flush()
    return {
        "trace_id": trace_id,
        "url": langfuse.get_trace_url(trace_id=trace_id),
        "question_id": question["id"],
        "prompt_version": "capability_guard",
        "answer": answer,
        "checks": checks,
        "judge": {"verdict": "not_run", "reason": "서비스 정책 응답: 생성·모델 평가 호출 없음"},
        "generation_ms": 0,
        "generation_load_ms": 0,
        "output_tokens": 0,
        "expected_score_names": names,
        "expected_observation_names": ["capability-check", "contract-checks"],
    }


def ensure_dataset(langfuse, incident=None):
    """Reuse identical cases; never overwrite a dataset that a student edited."""
    cases = regression_cases()
    version = hashlib.sha256(
        json.dumps(cases, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()[:10]
    name = "week11-release-" + version
    try:
        dataset = langfuse.get_dataset(name)
    except Exception as exc:
        if getattr(exc, "status_code", None) != 404:
            raise
        langfuse.create_dataset(
            name=name,
            description="반품·교환 상담 AI의 합성 회귀 평가 4건. 서비스 정확도 추정용이 아님.",
            metadata={"content_version": version, "synthetic_data": True},
        )
        for q in cases:
            langfuse.create_dataset_item(
                dataset_name=name,
                id=str(uuid.uuid5(uuid.NAMESPACE_URL, name + "/" + q["id"])),
                input={
                    "question_id": q["id"],
                    "question": q["query"],
                    "requested_capability": q["requested_capability"],
                },
                expected_output={
                    "answerable": q["answerable"],
                    "gold_ids": q["gold_ids"],
                    "reference": q["reference"],
                },
                metadata={
                    "intent_group": q["group"],
                    "role": "incident-regression" if q["id"] == "Q24a" else "normal-regression",
                },
                source_trace_id=incident["trace_id"] if incident and q["id"] == "Q24a" else None,
            )
        dataset = langfuse.get_dataset(name)
    expected = {q["id"]: q for q in cases}
    if len(dataset.items) != len(cases):
        raise ValueError(
            "원격 평가 데이터가 달라졌습니다. 기존 데이터를 덮어쓰지 말고 새 버전 이름을 사용하세요."
        )
    for item in dataset.items:
        q = expected.get(item.input.get("question_id"))
        if (
            not q
            or item.input.get("question") != q["query"]
            or item.input.get("requested_capability") != q["requested_capability"]
            or item.expected_output
            != {
                "answerable": q["answerable"],
                "gold_ids": q["gold_ids"],
                "reference": q["reference"],
            }
        ):
            raise ValueError(
                "원격 평가 데이터의 질문·참고 기준이 변경됐습니다. 새 버전으로 분리하세요."
            )
    return dataset


def evaluate_item(*, output, expected_output, **kwargs):
    if not isinstance(output, dict) or "answer" not in output:
        return Evaluation(
            name="execution_ok", value=0.0, comment="실행 오류도 평가에서 제외하지 않음"
        )
    checks = output["checks"]
    structural = all(v for v in checks.values() if v is not None)
    values = [
        Evaluation(name="execution_ok", value=1.0),
        Evaluation(
            name="structural_pass",
            value=float(structural),
            comment="인용·기권 계약 검사. 의미 정확도 아님",
        ),
        Evaluation(
            name="generation_ms",
            value=output["generation_ms"],
            comment="모델 생성 요청 경과 시간. 로컬 기기 관측값",
        ),
        Evaluation(
            name="llm_verdict",
            value=output["judge"]["verdict"],
            data_type="CATEGORICAL",
            comment=output["judge"]["reason"],
        ),
    ]
    if not expected_output["answerable"]:
        values.append(
            Evaluation(
                name="false_accept",
                value=float(not output["answer"]["abstain"]),
                comment="문서 밖 질문에서 응답을 시도했는지",
            )
        )
    return values


def run_version(langfuse, ollama, dataset, prompt_version):
    if prompt_version not in {*PROMPTS, "capability_guard"}:
        raise ValueError("지원하지 않는 실험 버전입니다.")
    by_id = {q["id"]: q for q in regression_cases()}

    def task(*, item, **kwargs):
        if prompt_version == "capability_guard":
            question = {
                **by_id[item.input["question_id"]],
                "requested_capability": item.input["requested_capability"],
            }
            return guarded_question(langfuse, ollama, question)
        return traced_question(
            langfuse, ollama, by_id[item.input["question_id"]], prompt_version=prompt_version
        )

    result = dataset.run_experiment(
        name="week11-" + prompt_version,
        task=task,
        evaluators=[evaluate_item],
        max_concurrency=1,
        metadata={
            "prompt_version": prompt_version,
            "prompt_sha256": hashlib.sha256(
                PROMPTS[
                    "grounded" if prompt_version == "capability_guard" else prompt_version
                ].encode()
            ).hexdigest(),
            "capability_policy": "capabilities-v1"
            if prompt_version == "capability_guard"
            else "none",
            "model": ollama.model,
            "model_digest": ollama.info["digest"],
            "retrieval": "char-current-k3",
            "suite": "teaching regression; not benchmark",
        },
    )
    langfuse.flush()
    rows = []
    for item in result.item_results:
        rows.append(
            {
                "question_id": item.item.input["question_id"],
                "trace_id": item.trace_id,
                "output": item.output,
                "evaluations": [
                    {"name": e.name, "value": e.value, "comment": e.comment}
                    for e in item.evaluations
                ],
            }
        )
    return {
        "version": prompt_version,
        "experiment_id": result.experiment_id,
        "experiment_url": result.experiment_url,
        "dataset": dataset.name,
        "rows": rows,
    }


def valid_output(output, question_id):
    if not isinstance(output, dict) or output.get("question_id") != question_id:
        return False
    checks = output.get("checks")
    required = {
        "citations_in_context",
        "citations_unique",
        "decision_matches_reference",
        "required_evidence_cited",
        "answer_citation_consistent",
    }
    if not isinstance(checks, dict) or set(checks) != required:
        return False
    if any(
        type(v) is not bool and not (k == "required_evidence_cited" and v is None)
        for k, v in checks.items()
    ):
        return False
    elapsed = output.get("generation_ms")
    return (
        isinstance(output.get("answer"), dict)
        and type(output["answer"].get("abstain")) is bool
        and isinstance(elapsed, (int, float))
        and math.isfinite(elapsed)
        and elapsed >= 0
        and isinstance(output.get("judge"), dict)
        and "verdict" in output["judge"]
    )


def release_decision(baseline, candidate, policy=None):
    """Missing/failed cases block release; judge scores cannot override hard failures."""
    policy = dict(policy or DEFAULT_POLICY)
    if baseline.get("dataset") != candidate.get("dataset"):
        return {
            "decision": "HOLD",
            "policy": policy,
            "reason": "서로 다른 평가 데이터",
            "checks": [],
        }
    expected = set(CASE_IDS)
    results = {}
    for label, experiment in [("baseline", baseline), ("candidate", candidate)]:
        rows = experiment["rows"]
        valid = (
            len(rows) == len(expected)
            and {r["question_id"] for r in rows} == expected
            and all(valid_output(r.get("output"), r["question_id"]) for r in rows)
        )
        if not valid:
            return {
                "decision": "HOLD",
                "policy": policy,
                "reason": f"{label}: 누락 또는 실패한 실행",
                "checks": [],
            }
        outputs = [r["output"] for r in rows]
        results[label] = {
            "structural_pass_rate": sum(
                all(v for v in o["checks"].values() if v is not None) for o in outputs
            )
            / len(outputs),
            "false_accepts": sum(
                not o["answer"]["abstain"] for o in outputs if o["question_id"] == "Q24a"
            ),
            "max_generation_ms": max(o["generation_ms"] for o in outputs),
            "llm_verdicts": [o["judge"]["verdict"] for o in outputs],
        }
    b, c = results["baseline"], results["candidate"]
    checks = [
        {
            "name": "답변 불가 수락 건수",
            "pass": c["false_accepts"] <= policy["max_false_accepts"],
            "value": c["false_accepts"],
        },
        {
            "name": "인용·기권 계약 통과율",
            "pass": c["structural_pass_rate"] >= policy["min_structural_pass_rate"],
            "value": c["structural_pass_rate"],
        },
        {
            "name": "기준선 대비 계약 검사 저하 없음",
            "pass": c["structural_pass_rate"] >= b["structural_pass_rate"],
            "value": c["structural_pass_rate"] - b["structural_pass_rate"],
        },
        {
            "name": "단일 생성 요청 시간 예산",
            "pass": c["max_generation_ms"] <= policy["max_generation_ms"],
            "value": c["max_generation_ms"],
        },
    ]
    return {
        "decision": "REVIEW" if all(c["pass"] for c in checks) else "HOLD",
        "policy": policy,
        "summary": results,
        "checks": checks,
        "reason": "필수 조건 통과 후에도 답변 내용의 사람 검토 필요. 자동 배포하지 않음.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--enforce-gate", action="store_true")
    args = parser.parse_args()
    lf, ollama = connect_langfuse(), OllamaClient()
    ollama.probe()
    try:
        incident = traced_question(lf, ollama, regression_cases()[-1], prompt_version="baseline")
        wait_for_trace(lf, incident)
        dataset = ensure_dataset(lf, incident)
        baseline = run_version(lf, ollama, dataset, "baseline")
        candidate = run_version(lf, ollama, dataset, "grounded")
        guarded = run_version(lf, ollama, dataset, "capability_guard")
        decision = release_decision(baseline, candidate)
        guarded_decision = release_decision(baseline, guarded)
        out = Path(__file__).with_name("reports") / "langfuse"
        out.mkdir(parents=True, exist_ok=True)
        (out / "release-comparison.json").write_text(
            json.dumps(
                {
                    "baseline": baseline,
                    "candidate": candidate,
                    "guarded": guarded,
                    "decision": decision,
                    "guarded_decision": guarded_decision,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(
            json.dumps(
                {
                    "dataset": dataset.name,
                    "experiments": [
                        baseline["experiment_url"],
                        candidate["experiment_url"],
                        guarded["experiment_url"],
                    ],
                    "decision": decision,
                    "guarded_decision": guarded_decision,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        if args.enforce_gate and decision["decision"] == "HOLD":
            raise SystemExit(2)
    finally:
        lf.shutdown()


if __name__ == "__main__":
    main()
