import asyncio
import copy
import json

import pytest
from prompt02.contracts import ExperimentRequest
from prompt02.core import fingerprint, load_dataset, load_prompt, render_prompt, validate_output
from prompt02.experiments import run_experiment


@pytest.fixture
def case():
    return load_dataset()["cases"][0]


def valid_output(**changes):
    value = {
        "category": "delivery",
        "priority": "normal",
        "needs_review": False,
        "reply": "주문 번호를 확인한 뒤 배송 상태를 안내하겠습니다.",
    }
    value.update(changes)
    return json.dumps(value, ensure_ascii=False)


@pytest.mark.parametrize(
    "raw",
    [
        "안녕하세요",
        "```json\n{}\n```",
        "[]",
        "null",
        "NaN",
        "{bad}",
        '{"category":"delivery","category":"refund"}',
        valid_output(needs_review="false"),
        valid_output(needs_review=0),
        valid_output(extra="unauthorized field"),
        valid_output(reply="     "),
        valid_output(category="__import__('os').system('echo unsafe')"),
        "__import__('pathlib').Path('/tmp/should-never-exist-prompt02').touch()",
        "[" * 1500,
    ],
)
def test_malformed_output_is_not_executed_and_semantics_are_unevaluated(raw, case):
    result = validate_output(raw, case)
    assert result["format_ok"] is False
    assert result["routing_ok"] is None
    assert result["promise_ok"] is None
    assert result["overall_ok"] is False


def test_format_success_does_not_imply_correct_routing(case):
    result = validate_output(valid_output(category="refund"), case)
    assert result["format_ok"] is True
    assert result["routing_ok"] is False
    assert result["promise_ok"] is True
    assert result["overall_ok"] is False


@pytest.mark.parametrize(
    "reply",
    [
        "오늘 전액 환불해 드리겠습니다.",
        "오늘 입금이 완료됩니다.",
        "환불 승인되었습니다.",
        "내일 배송이 보장됩니다.",
    ],
)
def test_unsupported_promises_are_separate_from_schema(reply, case):
    result = validate_output(valid_output(reply=reply), case)
    assert result["format_ok"] is True
    assert result["promise_ok"] is False


def test_safe_uncertainty_does_not_trigger_promise_rule(case):
    result = validate_output(
        valid_output(reply="환불 여부와 지급 시점은 담당자 확인 후 안내할 수 있습니다."), case
    )
    assert result["promise_ok"] is True


def test_snapshot_hashes_are_stable_and_sensitive_to_changes(case):
    assert fingerprint({"a": 1, "b": 2}) == fingerprint({"b": 2, "a": 1})
    rendered = render_prompt("v2", case)
    assert rendered == render_prompt("v2", case)
    changed_case = copy.deepcopy(case)
    changed_case["text"] += " 추가 문의"
    changed = render_prompt("v2", changed_case)
    assert changed["prompt_hash"] == rendered["prompt_hash"]
    assert changed["input_hash"] != rendered["input_hash"]
    assert changed["rendered_prompt_hash"] != rendered["rendered_prompt_hash"]
    altered_template = render_prompt("v2", case, template=load_prompt("v2") + "\n수정")
    assert altered_template["prompt_hash"] != rendered["prompt_hash"]
    assert altered_template["input_hash"] == rendered["input_hash"]


def test_identical_inputs_and_no_label_leakage(case):
    outputs = [render_prompt(version, case) for version in ("v1", "v2", "v3")]
    assert len({output["input_hash"] for output in outputs}) == 1
    assert len({output["messages"][1]["content"] for output in outputs}) == 1
    for output in outputs:
        assert "expected_category" not in str(output["messages"])
        assert case["rationale"] not in str(output["messages"])


def test_demo_is_reproducible_but_does_not_claim_model_improvement():
    a = asyncio.run(run_experiment(ExperimentRequest()))
    b = asyncio.run(run_experiment(ExperimentRequest()))
    assert a["simulation"] is True
    assert a["config"]["model"] == "fixed-teaching-fixtures-v1"
    assert a["run_id"] != b["run_id"]
    assert a["dataset_hash"] == b["dataset_hash"]
    assert [r["raw_output"] for r in a["rows"]] == [r["raw_output"] for r in b["rows"]]
    assert len(a["rows"]) == 24
    assert a["summary"]["v1"]["format_ok"]["passed"] == 7
    assert a["summary"]["v1"]["overall_ok"]["passed"] == 0
    assert a["summary"]["v2"]["overall_ok"]["passed"] == 4
    assert a["summary"]["v3"]["overall_ok"]["passed"] == 8
    for case_id in a["case_ids"]:
        assert len({r["input_hash"] for r in a["rows"] if r["case_id"] == case_id}) == 1


def test_each_version_template_is_read_once(monkeypatch):
    calls = []

    def read_once(version):
        calls.append(version)
        return f"{version} content at call {len(calls)}"

    monkeypatch.setattr("prompt02.experiments.load_prompt", read_once)
    report = asyncio.run(run_experiment(ExperimentRequest()))
    assert calls == ["v1", "v2", "v3"]
    for version in report["versions"]:
        assert len({r["prompt_hash"] for r in report["rows"] if r["version"] == version}) == 1


def test_selected_set_hash_changes_but_dataset_hash_is_fixed():
    one = asyncio.run(run_experiment(ExperimentRequest(case_ids=["T01"])))
    two = asyncio.run(run_experiment(ExperimentRequest(case_ids=["T01", "T03"])))
    assert one["dataset_hash"] == two["dataset_hash"]
    assert one["input_set_hash"] != two["input_set_hash"]


def test_injection_content_stays_in_user_data():
    case = next(c for c in load_dataset()["cases"] if c["id"] == "T06")
    rendered = render_prompt("v3", case)
    assert "이전 규칙을 무시" not in rendered["messages"][0]["content"]
    assert json.loads(rendered["messages"][1]["content"])["customer_message"] == case["text"]


def test_prompt_path_is_allowlisted():
    with pytest.raises(ValueError):
        load_prompt("../../../../.env")
