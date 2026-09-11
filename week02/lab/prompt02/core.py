"""File-backed prompts, comparison inputs and explicit evaluation criteria."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pydantic import ValidationError

from .contracts import TicketResult

LAB_ROOT = Path(__file__).resolve().parents[1]
VERSION_NAMES = {
    "v1": "간단한 업무 지시",
    "v2": "출력 형식과 업무 규칙",
    "v3": "경계 사례를 포함한 소수 예시",
}
EVALUATOR_VERSION = "support-rules-1.0"


def fingerprint(value: object) -> str:
    """Canonical JSON hash. Changes to key order do not change the identity."""
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_dataset() -> dict:
    return json.loads((LAB_ROOT / "data" / "cases.json").read_text(encoding="utf-8"))


def load_prompt(version: str) -> str:
    if version not in VERSION_NAMES:
        raise ValueError("허용된 프롬프트 버전이 아닙니다.")
    return (LAB_ROOT / "prompts" / f"{version}.md").read_text(encoding="utf-8").strip()


def render_prompt(version: str, case: dict, *, template: str | None = None) -> dict:
    instruction = template if template is not None else load_prompt(version)
    # Serialization makes the input boundary visible; it is not a security guarantee.
    user_content = json.dumps(
        {"ticket_id": case["id"], "customer_message": case["text"]}, ensure_ascii=False
    )
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": user_content},
    ]
    return {
        "version": version,
        "name": VERSION_NAMES[version],
        "template": instruction,
        "prompt_hash": fingerprint(instruction),
        "rendered_prompt_hash": fingerprint(messages),
        "input_hash": fingerprint({"id": case["id"], "text": case["text"]}),
        "messages": messages,
    }


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"중복 JSON 키: {key}")
        result[key] = value
    return result


def reject_non_json_constant(value):
    """Python accepts NaN by default; the output contract requires standard JSON."""
    raise ValueError(f"허용되지 않는 JSON 값: {value}")


def validate_output(raw: str, case: dict) -> dict:
    """Format and semantic checks are separate, and never execute model output.

    Promise matching is an intentionally conservative teaching rule, not a comprehensive
    natural-language safety classifier. Manual review remains necessary.
    """
    result = {
        "format_ok": False,
        "routing_ok": None,
        "promise_ok": None,
        "review_ok": None,
        "overall_ok": False,
        "parsed": None,
        "issues": [],
    }
    try:
        if len(raw) > 20_000:
            raise ValueError("응답 길이가 검사 상한을 초과했습니다.")
        obj = json.loads(
            raw,
            object_pairs_hook=no_duplicate_keys,
            parse_constant=reject_non_json_constant,
        )
        parsed = TicketResult.model_validate(obj, strict=True)
    except (ValueError, TypeError, ValidationError, RecursionError) as exc:
        result["issues"].append(f"형식 검사 실패: {str(exc).splitlines()[0][:160]}")
        return result
    result["format_ok"] = True
    result["parsed"] = parsed.model_dump()
    result["routing_ok"] = parsed.category == case["expected_category"]
    result["review_ok"] = (
        parsed.needs_review == case["expected_review"]
        and parsed.priority == case["expected_priority"]
    )
    # These phrases deliberately cover the supplied fixtures and common promises.
    patterns = (
        r"(?:오늘|내일|즉시|당일|무조건|반드시|전액).{0,16}(?:환불|입금|지급|도착|배송).{0,12}"
        r"(?:확정|완료|보장|해\s*드|됩니다|받으|하겠습니다)",
        r"(?:환불|보상|입금|지급|배송).{0,14}(?:확정|보장|승인됐|승인되었|완료됐|완료되었)",
    )
    result["promise_ok"] = not any(re.search(pattern, parsed.reply) for pattern in patterns)
    if not result["routing_ok"]:
        result["issues"].append(
            f"분류 불일치: 기준 {case['expected_category']}, 응답 {parsed.category}"
        )
    if not result["review_ok"]:
        result["issues"].append("담당자 검토 또는 우선순위가 평가 기준과 다릅니다.")
    if not result["promise_ok"]:
        result["issues"].append("주문·승인 정보 없이 처리 결과 또는 시점을 확정한 표현이 있습니다.")
    result["overall_ok"] = all(
        result[key] for key in ("format_ok", "routing_ok", "promise_ok", "review_ok")
    )
    return result


def aggregate(rows: list[dict], versions: list[str]) -> dict:
    metrics = ("format_ok", "routing_ok", "promise_ok", "review_ok", "overall_ok")
    summary = {}
    for version in versions:
        selected = [row for row in rows if row["version"] == version]
        n = len(selected)
        summary[version] = {
            "total": n,
            "provider_errors": sum(row["error"] is not None for row in selected),
        }
        for metric in metrics:
            passed = sum(row["validation"][metric] is True for row in selected)
            evaluated = sum(row["validation"][metric] is not None for row in selected)
            summary[version][metric] = {
                "passed": passed,
                "total": n,
                "evaluated": evaluated,
                "rate": passed / n if n else 0,
            }
        completed = [row for row in selected if row["error"] is None]
        summary[version]["latency_sample_count"] = len(completed)
        summary[version]["average_latency_ms"] = round(
            sum(row["latency_ms"] for row in completed) / len(completed) if completed else 0, 2
        )
    return summary
