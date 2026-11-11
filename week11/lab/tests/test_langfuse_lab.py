"""Optional platform profile: endpoint isolation, reproducible setup, and release gates."""

from copy import deepcopy

import pytest

pytest.importorskip("langfuse")
from week11.lab.langfuse.init_env import initialize
from week11.lab.langfuse_lab import local_settings
from week11.lab.release_lab import CASE_IDS, capability_response, release_decision


def test_init_keeps_existing_credentials_private(tmp_path):
    path, created = initialize(tmp_path)
    original = path.read_bytes()
    assert created
    assert initialize(tmp_path) == (path, False)
    assert path.read_bytes() == original
    assert (path.stat().st_mode & 0o077) == 0
    assert local_settings(path)["LANGFUSE_BASE_URL"] == "http://localhost:3011"


@pytest.mark.parametrize(
    "url",
    [
        "https://cloud.langfuse.com",
        "http://localhost.evil.test:3011",
        "http://user:pass@localhost:3011",
        "http://localhost:3011/api",
    ],
)
def test_cloud_and_credential_urls_rejected(tmp_path, url):
    p = tmp_path / ".env"
    p.write_text(f"LANGFUSE_BASE_URL={url}\nLANGFUSE_PUBLIC_KEY=pk\nLANGFUSE_SECRET_KEY=sk\n")
    with pytest.raises(ValueError):
        local_settings(p)


def experiment():
    rows = []
    for qid in CASE_IDS:
        abstain = qid == "Q24a"
        rows.append(
            {
                "question_id": qid,
                "output": {
                    "question_id": qid,
                    "answer": {"abstain": abstain},
                    "checks": {
                        "citations_in_context": True,
                        "citations_unique": True,
                        "decision_matches_reference": True,
                        "required_evidence_cited": None if abstain else True,
                        "answer_citation_consistent": True,
                    },
                    "generation_ms": 500,
                    "judge": {"verdict": "supported"},
                },
            }
        )
    return {"dataset": "same-frozen-suite", "rows": rows}


def test_all_gates_pass_still_requires_review():
    assert release_decision(experiment(), experiment())["decision"] == "REVIEW"


def test_judge_cannot_override_false_accept():
    candidate = experiment()
    row = candidate["rows"][-1]["output"]
    row["answer"]["abstain"] = False
    row["checks"]["decision_matches_reference"] = False
    assert row["judge"]["verdict"] == "supported"
    assert release_decision(experiment(), candidate)["decision"] == "HOLD"


@pytest.mark.parametrize(
    "damage", ["missing", "empty_checks", "nan_latency", "wrong_dataset", "duplicate"]
)
def test_missing_invalid_or_incomparable_evidence_blocks(damage):
    candidate = deepcopy(experiment())
    if damage == "missing":
        candidate["rows"].pop()
    elif damage == "empty_checks":
        candidate["rows"][0]["output"]["checks"] = {}
    elif damage == "nan_latency":
        candidate["rows"][0]["output"]["generation_ms"] = float("nan")
    elif damage == "wrong_dataset":
        candidate["dataset"] = "different-suite"
    else:
        candidate["rows"][0] = deepcopy(candidate["rows"][1])
    assert release_decision(experiment(), candidate)["decision"] == "HOLD"


def test_latency_budget_blocks_otherwise_passing_candidate():
    candidate = experiment()
    candidate["rows"][0]["output"]["generation_ms"] = 3001
    assert release_decision(experiment(), candidate)["decision"] == "HOLD"


def test_capability_policy_needs_no_reference_or_gold():
    assert capability_response("policy_qa") is None
    answer = capability_response("live_inventory")
    assert answer["abstain"] is True and answer["citations"] == []
    assert "확인할 수 없습니다" in answer["answer"]
    with pytest.raises(ValueError):
        capability_response("admin")
