"""File-backed evaluation rules. The rules are intentionally narrow teaching examples."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {
    "v0.1": "짧은 요약",
    "v0.2": "구조화 회의록",
}
EVALUATOR_VERSION = "minutes-rubric-1.0"
REQUIRED_SECTIONS = ("결정 사항", "실행 항목", "위험·확인 필요", "다음 단계")


def fingerprint(value: object) -> str:
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_dataset() -> dict:
    return json.loads((LAB_ROOT / "data" / "cases.json").read_text(encoding="utf-8"))


def load_prompt(version: str) -> str:
    if version not in VERSIONS:
        raise ValueError("허용된 프롬프트 버전이 아닙니다.")
    prompt_path = LAB_ROOT / "prompts" / f"meeting_minutes_{version}.md"
    return prompt_path.read_text(encoding="utf-8").strip()


def load_demo_outputs() -> dict:
    return json.loads((LAB_ROOT / "data" / "demo_outputs.json").read_text(encoding="utf-8"))


def cases_for_split(split: str) -> list[dict]:
    if split not in {"dev", "test"}:
        raise ValueError("dev 또는 test만 선택할 수 있습니다.")
    return [case for case in load_dataset()["cases"] if case["split"] == split]


def _sections(raw: str) -> dict[str, str]:
    headings = re.findall(r"^##\s+(.+?)\s*$", raw, flags=re.MULTILINE)
    return {heading: heading for heading in headings}


def _section_text(raw: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
    match = re.search(pattern, raw, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def evaluate(raw: str, case: dict) -> dict:
    """Score explicit contract, reference anchors, and action-item completeness.

    This evaluator deliberately does not claim to understand all Korean meeting minutes.
    It only makes the supplied rubric observable for this small synthetic teaching set.
    """
    result = {
        "structure_ok": False,
        "coverage_ok": None,
        "evidence_ok": None,
        "action_ok": None,
        "overall_ok": False,
        "issues": [],
        "found_sections": [],
    }
    if not raw or len(raw) > 12_000:
        result["issues"].append("출력 길이가 비어 있거나 평가 상한을 넘었습니다.")
        return result
    found = _sections(raw)
    result["found_sections"] = list(found)
    missing = [heading for heading in REQUIRED_SECTIONS if heading not in found]
    if missing:
        result["issues"].append("필수 섹션 누락: " + ", ".join(missing))
        return result
    result["structure_ok"] = True
    anchors = case["expected"]["anchors"]
    absent = [anchor for anchor in anchors if anchor not in raw]
    result["coverage_ok"] = not absent
    if absent:
        result["issues"].append("핵심 사실 누락: " + ", ".join(absent))
    banned = case["expected"].get("banned_claims", [])
    present_banned = [claim for claim in banned if claim in raw]
    result["evidence_ok"] = not present_banned
    if present_banned:
        result["issues"].append("원문 근거 없는 단정: " + ", ".join(present_banned))
    actions = _section_text(raw, "실행 항목")
    action_markers = case["expected"]["action_markers"]
    missing_action = [marker for marker in action_markers if marker not in actions]
    result["action_ok"] = not missing_action
    if missing_action:
        result["issues"].append("실행 항목 정보 누락: " + ", ".join(missing_action))
    result["overall_ok"] = all(
        result[key] for key in ("structure_ok", "coverage_ok", "evidence_ok", "action_ok")
    )
    return result


def aggregate(rows: list[dict], versions: list[str]) -> dict:
    metrics = ("structure_ok", "coverage_ok", "evidence_ok", "action_ok", "overall_ok")
    result = {}
    for version in versions:
        selected = [row for row in rows if row["version"] == version]
        result[version] = {"total": len(selected)}
        for metric in metrics:
            passed = sum(row["evaluation"][metric] is True for row in selected)
            evaluated = sum(row["evaluation"][metric] is not None for row in selected)
            result[version][metric] = {
                "passed": passed,
                "evaluated": evaluated,
                "total": len(selected),
                "rate": passed / len(selected) if selected else 0,
            }
    return result
