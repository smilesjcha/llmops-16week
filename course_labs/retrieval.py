"""Readable retrieval algorithms. Synthetic corpus; no network or model downloads.

TF-IDF and BM25 here are lexical baselines, NOT neural dense embeddings.
Synonym expansion and rule reranking are explicit educational heuristics.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from time import perf_counter

DATA = Path(__file__).parent / "data"


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    text: str
    version: str = "1.0"
    access: str = "public"
    valid_from: str = "2026-01-01"
    valid_to: str | None = None
    source: str = "교육용 합성 정책"


@dataclass(frozen=True)
class Chunk:
    id: str
    doc_id: str
    title: str
    text: str
    start: int
    end: int
    version: str
    access: str
    valid_from: str
    valid_to: str | None


def load_documents() -> list[Document]:
    return [Document(**d) for d in json.loads((DATA / "documents.json").read_text())]


def load_cases() -> list[dict]:
    return json.loads((DATA / "queries.json").read_text())


def chunk_document(doc: Document, size: int = 120, overlap: int = 24) -> list[Chunk]:
    """Character windows with exact offsets. Production uses tokenizer-aware splits."""
    if not isinstance(size, int) or not isinstance(overlap, int) or not 0 <= overlap < size:
        raise ValueError("0 <= overlap < size, both integers")
    chunks = []
    start = 0
    while start < len(doc.text):
        end = min(start + size, len(doc.text))
        chunks.append(
            Chunk(
                f"{doc.id}:c{len(chunks):02d}",
                doc.id,
                doc.title,
                doc.text[start:end],
                start,
                end,
                doc.version,
                doc.access,
                doc.valid_from,
                doc.valid_to,
            )
        )
        if end == len(doc.text):
            break
        start = end - overlap
    return chunks


def tokenize(text: str, ngrams: bool = True) -> list[str]:
    """Whitespace words + Korean 2/3 character grams. No morphological claims."""
    words = re.findall(r"[a-z0-9]+|[가-힣]+", text.lower())
    terms = list(words)
    if ngrams:
        for word in words:
            if re.fullmatch(r"[가-힣]+", word):
                for n in (2, 3):
                    terms += [word[i : i + n] for i in range(len(word) - n + 1)]
    return terms


ALIASES = {
    "되돌려": "반품",
    "돌려보내": "반품",
    "취소": "환불",
    "배송료": "배송비",
    "돈": "환불",
    "갈아": "교환",
    "사이즈": "크기",
    "자료": "문서",
    "근거": "출처",
}


def expand_query(query: str, aliases: dict | None = None) -> str:
    mapping = ALIASES if aliases is None else aliases
    added = [v for k, v in mapping.items() if k in query and v not in query]
    return " ".join([query, *dict.fromkeys(added)])


def eligible_chunks(chunks: list[Chunk], as_of: str, role: str = "public") -> list[Chunk]:
    """Inclusive start, exclusive end. Fail closed for unrecognised role/access."""
    date.fromisoformat(as_of)
    if role not in {"public", "staff"}:
        raise ValueError("Unknown role")
    return [
        c
        for c in chunks
        if c.valid_from <= as_of
        and (c.valid_to is None or as_of < c.valid_to)
        and (c.access == "public" or (c.access == "staff" and role == "staff"))
    ]


class LexicalIndex:
    def __init__(self, chunks: list[Chunk], ngrams: bool = True):
        self.chunks = chunks
        self.counts = [Counter(tokenize(c.title + " " + c.text, ngrams)) for c in chunks]
        self.ngrams = ngrams
        self.df = Counter(t for counts in self.counts for t in counts)
        self.n = len(chunks)
        self.lengths = [sum(c.values()) for c in self.counts]
        self.avgdl = sum(self.lengths) / self.n if self.n else 1

    def search(
        self, query: str, method: str = "bm25", k: int = 5, k1: float = 1.5, b: float = 0.75
    ) -> list[dict]:
        if method not in {"bm25", "tfidf"}:
            raise ValueError("method must be bm25 or tfidf")
        if k < 1 or k1 <= 0 or not 0 <= b <= 1:
            raise ValueError("Invalid search parameters")
        q = Counter(tokenize(query, self.ngrams))

        def idf(term):
            return math.log((self.n + 1) / (self.df[term] + 1)) + 1

        qvec = {t: (1 + math.log(f)) * idf(t) for t, f in q.items()}
        qnorm = math.sqrt(sum(v * v for v in qvec.values()))
        ranked = []
        for chunk, counts, dl in zip(self.chunks, self.counts, self.lengths, strict=False):
            if method == "bm25":
                score = 0.0
                for t in q:
                    f = counts[t]
                    if f:
                        weight = math.log(1 + (self.n - self.df[t] + 0.5) / (self.df[t] + 0.5))
                        score += weight * f * (k1 + 1) / (f + k1 * (1 - b + b * dl / self.avgdl))
            else:
                vec = {t: (1 + math.log(f)) * idf(t) for t, f in counts.items()}
                norm = math.sqrt(sum(v * v for v in vec.values()))
                score = (
                    sum(v * vec.get(t, 0) for t, v in qvec.items()) / (norm * qnorm)
                    if norm and qnorm
                    else 0.0
                )
            if score > 0:
                ranked.append({"chunk": asdict(chunk), "score": score, "method": method})
        return sorted(ranked, key=lambda r: (-r["score"], r["chunk"]["id"]))[:k]


def reciprocal_rank_fusion(
    rankings: list[list[dict]], constant: int = 60, k: int = 5
) -> list[dict]:
    if constant < 1 or k < 1:
        raise ValueError("constant and k must be positive")
    scores, records = Counter(), {}
    for ranking in rankings:
        seen = set()
        for rank, hit in enumerate(ranking, 1):
            cid = hit["chunk"]["id"]
            if cid not in seen:
                scores[cid] += 1 / (constant + rank)
                records[cid] = hit
                seen.add(cid)
    return [
        {**records[cid], "score": scores[cid], "method": "rrf"}
        for cid in sorted(scores, key=lambda x: (-scores[x], x))[:k]
    ]


def rerank_by_coverage(query: str, hits: list[dict], k: int = 5) -> list[dict]:
    """Rule reranker, not a trained cross-encoder. Keep original rank for ties."""
    terms = set(tokenize(query))
    scored = []
    for rank, hit in enumerate(hits):
        coverage = len(terms & set(tokenize(hit["chunk"]["text"]))) / len(terms) if terms else 0
        scored.append(
            {
                **hit,
                "retrieval_score": hit["score"],
                "score": coverage,
                "method": "coverage-rule",
                "original_rank": rank + 1,
            }
        )
    return sorted(scored, key=lambda x: (-x["score"], x["original_rank"]))[:k]


def retrieval_metrics(
    retrieved_doc_ids: list[str], relevant_doc_ids: list[str], k: int = 3
) -> dict:
    """Deduplicated document-level metrics. No-answer queries are separate."""
    if k < 1:
        raise ValueError("k must be positive")
    unique = list(dict.fromkeys(retrieved_doc_ids))[:k]
    relevant = set(relevant_doc_ids)
    if not relevant:
        return {"recall": None, "mrr": None, "hit": None, "precision": None}
    matches = len(set(unique) & relevant)
    first = next((i for i, d in enumerate(unique, 1) if d in relevant), None)
    return {
        "recall": matches / len(relevant),
        "mrr": 1 / first if first else 0,
        "hit": float(matches > 0),
        "precision": matches / k,
    }


def retrieve(
    query: str,
    docs: list[Document] | None = None,
    *,
    size=120,
    overlap=24,
    as_of="2026-09-29",
    role="public",
    method="bm25",
    k=3,
    expand=False,
    rerank=False,
    ngrams=True,
) -> dict:
    started = perf_counter()
    docs = load_documents() if docs is None else docs
    all_chunks = [c for d in docs for c in chunk_document(d, size, overlap)]
    chunks = eligible_chunks(all_chunks, as_of, role)
    index = LexicalIndex(chunks, ngrams)
    prepared = expand_query(query) if expand else query
    if method == "rrf":
        hits = reciprocal_rank_fusion(
            [index.search(prepared, m, max(k * 3, 8)) for m in ("bm25", "tfidf")], k=max(k * 3, 8)
        )
    else:
        hits = index.search(prepared, method, max(k * 3, 8))
    if rerank:
        hits = rerank_by_coverage(prepared, hits, max(k * 3, 8))
    # Unique documents: duplicate windows must not inflate Recall@k.
    unique, seen = [], set()
    for h in hits:
        if h["chunk"]["doc_id"] not in seen:
            unique.append(h)
            seen.add(h["chunk"]["doc_id"])
        if len(unique) == k:
            break
    return {
        "query": query,
        "prepared_query": prepared,
        "hits": unique,
        "eligible_chunks": len(chunks),
        "excluded_chunks": len(all_chunks) - len(chunks),
        "elapsed_ms": (perf_counter() - started) * 1000,
        "config": {
            "size": size,
            "overlap": overlap,
            "as_of": as_of,
            "role": role,
            "method": method,
            "k": k,
            "expand": expand,
            "rerank": rerank,
        },
        "corpus_hash": hashlib.sha256(
            json.dumps([asdict(d) for d in docs], ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest()[:16],
    }


def answer_from_evidence(report: dict, minimum_coverage: float = 0.25) -> dict:
    """Extractive preview only. Overlap is a weak heuristic, NOT factual confidence."""
    if not 0 <= minimum_coverage <= 1:
        raise ValueError("coverage must be in [0,1]")
    qterms = set(tokenize(report["prepared_query"]))
    best = report["hits"][0] if report["hits"] else None
    coverage = (
        len(qterms & set(tokenize(best["chunk"]["text"]))) / len(qterms) if best and qterms else 0
    )
    if not best or coverage < minimum_coverage:
        return {
            "status": "abstain",
            "text": "확인 가능한 근거가 부족합니다. 문서 또는 질문을 추가해 주세요.",
            "citations": [],
            "term_coverage": coverage,
            "mode": "extractive-preview",
        }
    chunk = best["chunk"]
    return {
        "status": "evidence-preview",
        "text": chunk["text"],
        "citations": [
            {
                "doc_id": chunk["doc_id"],
                "chunk_id": chunk["id"],
                "title": chunk["title"],
                "version": chunk["version"],
                "start": chunk["start"],
                "end": chunk["end"],
            }
        ],
        "term_coverage": coverage,
        "mode": "extractive-preview",
    }


def evaluate(cases: list[dict] | None = None, **config) -> dict:
    """Per-case role/date preserve the evaluation target; search settings may vary."""
    cases = load_cases() if cases is None else cases
    rows = []
    for c in cases:
        options = {**config, "role": c.get("role", "public"), "as_of": c.get("as_of", "2026-09-29")}
        report = retrieve(c["query"], **options)
        ids = [h["chunk"]["doc_id"] for h in report["hits"]]
        metrics = retrieval_metrics(ids, c["relevant"], config.get("k", 3))
        answer = answer_from_evidence(report)
        rows.append(
            {
                "id": c["id"],
                "split": c["split"],
                "query": c["query"],
                "role": options["role"],
                "as_of": options["as_of"],
                "relevant": c["relevant"],
                "retrieved": ids,
                **metrics,
                "abstained": answer["status"] == "abstain",
                "elapsed_ms": report["elapsed_ms"],
            }
        )
    answerable = [r for r in rows if r["recall"] is not None]
    unanswerable = [r for r in rows if r["recall"] is None]
    return {
        "rows": rows,
        "config": config,
        "summary": {
            "answerable_count": len(answerable),
            "no_answer_count": len(unanswerable),
            "recall": sum(r["recall"] for r in answerable) / len(answerable)
            if answerable
            else None,
            "mrr": sum(r["mrr"] for r in answerable) / len(answerable) if answerable else None,
            "answerable_abstention": sum(r["abstained"] for r in answerable) / len(answerable)
            if answerable
            else None,
            "correct_abstention": sum(r["abstained"] for r in unanswerable) / len(unanswerable)
            if unanswerable
            else None,
        },
    }
