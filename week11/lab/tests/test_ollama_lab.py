"""Transport and contract tests; actual inference is verified separately."""

import pytest
import requests
from week11.lab.ollama_lab import (
    OllamaClient,
    OllamaError,
    inspect_answer,
    validate_answer,
    generate_one,
)


def test_remote_or_credential_url_rejected():
    for url in [
        "https://example.com",
        "http://key:secret@localhost:11434",
        "http://localhost:11434/path",
        "http://localhost:11434?x=y",
    ]:
        with pytest.raises(ValueError):
            OllamaClient(base_url=url)


def test_timeout_is_actionable_and_never_falls_back(monkeypatch):
    c = OllamaClient()

    def timeout(*args, **kwargs):
        raise requests.Timeout()

    monkeypatch.setattr(c.session, "request", timeout)
    with pytest.raises(OllamaError, match="시간 초과"):
        c.probe()


@pytest.mark.parametrize(
    "value",
    [
        {},
        [],
        {"answer": "", "citations": [], "abstain": False},
        {"answer": "x", "citations": "D01", "abstain": False},
        {"answer": "x", "citations": [], "abstain": "false"},
    ],
)
def test_answer_contract_rejects_invalid_model_output(value):
    with pytest.raises(OllamaError):
        validate_answer(value)


def test_citations_not_equivalent_to_correctness():
    answer = {"answer": "틀린 답", "citations": ["D99", "D99"], "abstain": False}
    checks = inspect_answer(answer, [{"id": "D01"}], ["D01"], True)
    assert not checks["citations_in_context"]
    assert not checks["citations_unique"]
    assert not checks["required_evidence_cited"]
    assert "accuracy" not in checks


def test_unanswerable_checks_do_not_invent_recall():
    checks = inspect_answer({"answer": "모름", "citations": [], "abstain": True}, [], [], False)
    assert checks["decision_matches_reference"]
    assert checks["required_evidence_cited"] is None


def test_reference_answer_never_sent_to_generator():
    class RecordingClient:
        model = "test-transport-only"

        def chat(self, messages, schema):
            assert "SECRET_GOLD" not in str(messages)
            assert "SECRET_REFERENCE" not in str(messages)
            return {
                "parsed": {"answer": "검사용", "citations": [], "abstain": True},
                "latency_ms": 1,
            }

    row = generate_one(
        RecordingClient(),
        {
            "id": "unit",
            "query": "반품 기간",
            "gold_ids": ["SECRET_GOLD"],
            "answerable": True,
            "reference": "SECRET_REFERENCE",
        },
    )
    assert row["spans"][0]["name"] == "retrieval"
