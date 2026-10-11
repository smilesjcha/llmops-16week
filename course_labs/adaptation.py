"""Offline teaching experiments, not LLM training or a grading system."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from html import escape
from pathlib import Path

import numpy as np


def examples(n: int = 24) -> list[dict]:
    """Synthetic support cases; each case has two related paraphrases."""
    if n < 3:
        raise ValueError("at least three groups required")
    return [
        {"id": f"E{i:02}-{j}", "group": f"case-{i:02}",
         "instruction": f"합성 문의 {i}의 처리 상태를 JSON으로 정리",
         "input": f"사례 {i} / 표현 {j} / 참조 문서 DEMO-{i:02}",
         "response": json.dumps({"status": "review", "source": f"DEMO-{i:02}"}),
         "synthetic": True}
        for i in range(n) for j in range(2)
    ]


def audit(records: list[dict]) -> dict:
    issues = []
    ids, fingerprints = Counter(), Counter()
    for index, row in enumerate(records):
        for key in ("id", "group", "instruction", "input", "response"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                issues.append({"row": index, "kind": "missing", "field": key})
        if row.get("synthetic") is not True:
            issues.append({"row": index, "kind": "permission_review", "field": "synthetic"})
        ids[str(row.get("id"))] += 1
        fingerprint = json.dumps([row.get(k) for k in ("instruction", "input", "response")], ensure_ascii=False)
        fingerprints[hashlib.sha256(fingerprint.encode()).hexdigest()] += 1
        try:
            answer = json.loads(row.get("response", ""))
            if not isinstance(answer, dict) or set(answer) != {"status", "source"}:
                raise ValueError("schema")
        except (ValueError, TypeError):
            issues.append({"row": index, "kind": "invalid_output", "field": "response"})
    return {"rows": len(records), "issues": issues,
            "duplicate_ids": [k for k, v in ids.items() if v > 1],
            "duplicate_content": sum(v - 1 for v in fingerprints.values() if v > 1)}


def split_groups(records: list[dict], seed: int = 42) -> dict[str, list[dict]]:
    groups = sorted({row["group"] for row in records})
    if len(groups) < 3:
        raise ValueError("train/dev/test each need at least one group")
    order = np.random.default_rng(seed).permutation(groups).tolist()
    dev_count = max(1, len(groups) // 6)
    test_count = max(1, len(groups) // 6)
    membership = {g: "dev" for g in order[:dev_count]}
    membership.update({g: "test" for g in order[dev_count:dev_count + test_count]})
    return {name: [dict(r) for r in records if membership.get(r["group"], "train") == name]
            for name in ("train", "dev", "test")}


def leakage(splits: dict[str, list[dict]]) -> list[dict]:
    result = []
    names = list(splits)
    for i, left in enumerate(names):
        for right in names[i + 1:]:
            shared = sorted({r["group"] for r in splits[left]} & {r["group"] for r in splits[right]})
            if shared:
                result.append({"left": left, "right": right, "shared_groups": shared})
    return result


def rank_approximation(matrix: np.ndarray, rank: int) -> dict:
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or not np.isfinite(matrix).all():
        raise ValueError("finite 2D matrix required")
    if not isinstance(rank, int) or not 1 <= rank <= min(matrix.shape):
        raise ValueError("invalid rank")
    u, s, vt = np.linalg.svd(matrix, full_matrices=False)
    b = u[:, :rank] * s[:rank]
    a = vt[:rank]
    reconstructed = b @ a
    denom = np.linalg.norm(matrix)
    return {"a": a, "b": b, "update": reconstructed,
            "full_params": matrix.size, "factor_params": rank * sum(matrix.shape),
            "relative_error": float(np.linalg.norm(matrix - reconstructed) / denom) if denom else 0.0}


def dpo_loss(policy_chosen: float, policy_rejected: float,
             reference_chosen: float, reference_rejected: float, beta: float = .1) -> float:
    """Inputs are sequence log-probabilities, not raw probabilities or judge scores."""
    values = [policy_chosen, policy_rejected, reference_chosen, reference_rejected, beta]
    if not np.isfinite(values).all() or beta <= 0:
        raise ValueError("finite values and positive beta required")
    margin = (policy_chosen - policy_rejected) - (reference_chosen - reference_rejected)
    return float(np.logaddexp(0, -beta * margin))


def toy_preference_training(beta: float = .5, steps: int = 80, lr: float = .3) -> list[dict]:
    """One prompt, two fixed responses, Bernoulli policy; no language model."""
    if beta <= 0 or lr <= 0 or steps < 1:
        raise ValueError("positive configuration required")
    theta, theta_ref = 0.0, 0.0
    records = []
    for step in range(steps + 1):
        p = float(1 / (1 + np.exp(-theta)))
        loss = dpo_loss(np.log(p), np.log1p(-p), np.log(.5), np.log(.5), beta)
        records.append({"step": step, "chosen_probability": p, "loss": loss, "theta": theta})
        gradient = -beta * np.exp(-np.logaddexp(0, beta * (theta - theta_ref)))
        theta -= lr * gradient
    return records


def preference_audit(rows: list[dict]) -> list[dict]:
    issues = []
    for i, r in enumerate(rows):
        for k in ("prompt", "chosen", "rejected", "reason"):
            if not isinstance(r.get(k), str) or not r[k].strip():
                issues.append({"row": i, "kind": "missing", "field": k})
        if r.get("chosen") == r.get("rejected"):
            issues.append({"row": i, "kind": "identical_pair"})
    return issues


def proposal_check(doc: dict) -> list[str]:
    """Presence check only. Does not assess feasibility or assign a grade."""
    required = ("user", "problem", "baseline", "scope", "data_rights", "evaluation", "fallback", "roadmap", "question")
    return [key for key in required if not isinstance(doc.get(key), str) or not doc[key].strip()]


def proposal_html(doc: dict) -> str:
    labels = {"user": "대상 사용자", "problem": "문제와 제안", "baseline": "현재 대안", "scope": "최소 기능과 제외 범위", "data_rights": "데이터·권한", "evaluation": "평가 계획", "fallback": "실패·보류·복구", "roadmap": "일정과 담당", "question": "교수에게 확인할 질문"}
    body = "".join(f"<section><h2>{escape(label)}</h2><p>{escape(str(doc.get(key, '미작성')))}</p></section>" for key, label in labels.items())
    return '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>기획서 초안 0.1</title><style>body{max-width:900px;margin:40px auto;padding:24px;font:18px/1.7 sans-serif;color:#17191b}h1{font-size:36px}h2{font-size:22px;border-top:1px solid #ccc;padding-top:18px}p{white-space:pre-wrap}@media print{body{margin:0}section{break-inside:avoid}}</style><h1>서비스 기획서 초안 0.1</h1><p>작성용 시안 · 자동 생성 결과는 검토 후 제출 · 개인정보 공개 금지</p>' + body + '</html>'


def save_report(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
