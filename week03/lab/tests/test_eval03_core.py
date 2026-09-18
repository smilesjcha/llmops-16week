import copy

import pytest
from eval03.core import (
    cases_for_split,
    evaluate,
    fingerprint,
    load_dataset,
    load_demo_outputs,
    load_prompt,
)


def test_dataset_has_separate_dev_and_test_cases():
    assert [case["id"] for case in cases_for_split("dev")] == ["M01", "M02", "M03", "M04"]
    assert [case["id"] for case in cases_for_split("test")] == ["M05", "M06"]
    with pytest.raises(ValueError):
        cases_for_split("all")


def test_v01_fails_structure_before_semantic_checks():
    case = cases_for_split("dev")[0]
    result = evaluate(load_demo_outputs()[case["id"]]["v0.1"], case)
    assert result["structure_ok"] is False
    assert result["coverage_ok"] is None
    assert result["evidence_ok"] is None
    assert result["action_ok"] is None
    assert result["overall_ok"] is False


def test_v02_can_separate_missing_action_data_from_other_checks():
    case = next(case for case in cases_for_split("dev") if case["id"] == "M02")
    result = evaluate(load_demo_outputs()["M02"]["v0.2"], case)
    assert result["structure_ok"] is True
    assert result["coverage_ok"] is True
    assert result["evidence_ok"] is True
    assert result["action_ok"] is False


def test_v02_detects_explicit_unsupported_claim():
    case = next(case for case in cases_for_split("dev") if case["id"] == "M03")
    result = evaluate(load_demo_outputs()["M03"]["v0.2"], case)
    assert result["structure_ok"] is True
    assert result["evidence_ok"] is False
    assert "예산 승인 완료" in " ".join(result["issues"])


def test_hash_is_stable_and_data_change_is_visible():
    dataset = load_dataset()
    assert fingerprint({"a": 1, "b": 2}) == fingerprint({"b": 2, "a": 1})
    changed = copy.deepcopy(dataset)
    changed["cases"][0]["transcript"] += " 변경"
    assert fingerprint(dataset) != fingerprint(changed)


def test_prompt_versions_are_allowlisted():
    assert "구조화된 회의록" in load_prompt("v0.2")
    with pytest.raises(ValueError):
        load_prompt("../../.env")
