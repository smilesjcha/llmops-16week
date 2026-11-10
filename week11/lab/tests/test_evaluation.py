import pytest
from sklearn.metrics import ndcg_score
from week11.lab.evaluation import (
    Config, Retriever, evaluate, load_data, paired_group_bootstrap, ranking_metrics,
    release_gate, select_on_dev, summarize, validate_data,
)
from week11.lab.judging import validate_judge_json, agreement, order_consistency


def test_metrics_match_hand_calculation_and_independent_library():
    r = ranking_metrics(["X", "A", "B"], ["A", "B"], 3)
    assert r["hit"] == r["recall"] == 1
    assert r["mrr"] == 0.5
    assert r["ndcg"] == pytest.approx(ndcg_score([[0, 1, 1]], [[3, 2, 1]], k=3))
    assert ranking_metrics(["A", "X"], ["A", "B"], 2)["recall"] == 0.5


def test_unanswerable_and_empty_retrieval_are_distinct():
    assert all(v is None for v in ranking_metrics([], [], 3).values())
    assert all(v == 0 for v in ranking_metrics([], ["A"], 3).values())
    assert summarize([])["recall"] is None


@pytest.mark.parametrize("ranked,k", [(["A", "A"], 2), (["A"], 0)])
def test_invalid_rankings_rejected(ranked, k):
    with pytest.raises(ValueError):
        ranking_metrics(ranked, ["A"], k)


def test_group_leakage_rejected():
    docs, qs = load_data()
    qs[1]["split"] = "test"
    with pytest.raises(ValueError, match="leakage"):
        validate_data(docs, qs)


@pytest.mark.parametrize("field,value", [("gold_ids", ["MISSING"]), ("answerable", False), ("query", "")])
def test_invalid_case_rejected(field, value):
    docs, qs = load_data()
    qs[0][field] = value
    with pytest.raises(ValueError):
        validate_data(docs, qs)


def test_index_does_not_learn_query_and_removes_archive():
    docs, _ = load_data()
    retriever = Retriever(docs, Config("test", "char", True))
    vocab = dict(retriever.vectorizer.vocabulary_)
    assert not retriever.search("zzzzzzzz")
    assert retriever.vectorizer.vocabulary_ == vocab
    assert all(d["status"] == "current" for d in retriever.docs)


def test_ties_are_stable_and_positive_only():
    doc = dict(title="반품", text="반품", status="current")
    retriever = Retriever([{**doc, "id": "B"}, {**doc, "id": "A"}], Config("ties"))
    assert [h["id"] for h in retriever.search("반품")] == ["A", "B"]
    assert retriever.search("없는단어") == []


def test_no_answer_denominators_and_threshold():
    docs, qs = load_data()
    s = summarize(evaluate(docs, qs, Config("abstain", "char", True, 3, 1.0)))
    assert s["answerable_n"] == 32 and s["unanswerable_n"] == 16
    assert s["coverage"] == s["false_accept"] == 0
    assert s["missed_answer"] == 1


def test_tuner_rejects_test_set():
    docs, qs = load_data()
    with pytest.raises(ValueError, match="dev"):
        select_on_dev(docs, qs)


def test_bootstrap_pairs_ids_not_row_positions():
    a = [dict(id=str(i), group=str(i // 2), recall=0.0) for i in range(6)]
    b = [{**r, "recall": 0.5} for r in reversed(a)]
    ci = paired_group_bootstrap(a, b, n_boot=100)
    assert ci["groups"] == 3
    assert ci["delta"] == ci["low"] == ci["high"] == 0.5
    with pytest.raises(ValueError):
        paired_group_bootstrap(a, b[:-1])


def test_gate_does_not_reward_total_abstention():
    baseline = {"recall": 0.7}
    candidate = {"recall": 0.8, "false_accept": 0.0, "evidence_complete": 0.0}
    assert release_gate(baseline, candidate, {"low": 0.0})["decision"] == "HOLD"


@pytest.mark.parametrize("raw", ['[]', '{}', '{"verdict":"good","reason":"x"}', '{"verdict":"supported","reason":""}'])
def test_judge_schema_rejects_invalid_output(raw):
    with pytest.raises(ValueError):
        validate_judge_json(raw)


def test_authored_agreement_and_order():
    assert agreement()["agreement"] == 5 / 8
    assert order_consistency([dict(winner_ab="answer1", winner_ba="answer1")]) == 1
    assert order_consistency([]) is None
