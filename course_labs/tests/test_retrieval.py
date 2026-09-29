import pytest
from fastapi.testclient import TestClient

from course_labs.retrieval import (
    Document,
    answer_from_evidence,
    chunk_document,
    evaluate,
    reciprocal_rank_fusion,
    retrieval_metrics,
    retrieve,
)
from course_labs.webapp import create_app


def test_offsets_and_overlap():
    doc = Document("x", "t", "abcdefghij")
    chunks = chunk_document(doc, 4, 1)
    assert [c.text for c in chunks] == ["abcd", "defg", "ghij"]
    assert all(doc.text[c.start : c.end] == c.text for c in chunks)
    for size, overlap in [(0, 0), (4, 4), (4, -1)]:
        with pytest.raises(ValueError):
            chunk_document(doc, size, overlap)


@pytest.mark.parametrize("method", ["bm25", "tfidf", "rrf"])
def test_permission_and_time_before_search(method):
    r = retrieve("내부 승인 티켓 EX-77 반품", method=method, k=8)
    ids = {h["chunk"]["doc_id"] for h in r["hits"]}
    assert not ids & {"D08", "D09", "D18"}
    assert retrieve("상품 반품 기간", as_of="2026-08-15")["hits"][0]["chunk"]["doc_id"] == "D08"
    assert retrieve("내부 승인 티켓 EX-77", role="staff")["hits"][0]["chunk"]["doc_id"] == "D09"


def test_no_evidence_abstain():
    r = retrieve("화성 우주 정거장 운임")
    assert answer_from_evidence(r)["status"] == "abstain"
    assert not answer_from_evidence(r)["citations"]


def test_metrics_and_duplicates():
    assert retrieval_metrics(["a", "a", "b"], ["a", "b"], 2) == {
        "recall": 1,
        "mrr": 1,
        "hit": 1,
        "precision": 1,
    }
    assert retrieval_metrics(["b", "a"], ["a"], 2)["mrr"] == 0.5
    assert retrieval_metrics([], [], 3)["recall"] is None


def test_rrf_score():
    h = {"chunk": {"id": "a"}, "score": 9}
    assert reciprocal_rank_fusion([[h, h], [h]], 60)[0]["score"] == pytest.approx(2 / 61)


@pytest.mark.parametrize("week", [4, 5])
def test_api(week):
    c = TestClient(create_app(week))
    assert c.get("/health").json()["week"] == week
    assert c.get("/").status_code == 200
    r = c.post("/api/search", json={"query": "상품 반품 기간"})
    assert r.status_code == 200 and r.json()["answer"]["citations"]
    assert (
        c.post("/api/search", json={"query": "x", "overlap": 150, "size": 120}).status_code == 422
    )
    assert c.post("/api/search", json={"query": "x", "as_of": "not-date"}).status_code == 422
    assert (
        c.post("/api/evaluate", json={"query": "eval", "method": "rrf"}).json()["summary"][
            "answerable_count"
        ]
        == 13
    )


def test_json_determinism():
    a, b = retrieve("교환 신청"), retrieve("교환 신청")
    assert a["hits"] == b["hits"]
    assert a["corpus_hash"] == b["corpus_hash"]


def test_abstention_metrics_separate_answerable_questions():
    result = evaluate()
    answerable = [r for r in result["rows"] if r["relevant"]]
    unanswered = [r for r in result["rows"] if not r["relevant"]]
    assert result["summary"]["answerable_abstention"] == pytest.approx(
        sum(r["abstained"] for r in answerable) / len(answerable)
    )
    assert result["summary"]["correct_abstention"] == pytest.approx(
        sum(r["abstained"] for r in unanswered) / len(unanswered)
    )
