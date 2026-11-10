"""Inspectable offline retrieval evaluation. No model calls, no production claims."""
from __future__ import annotations

import hashlib
import json
import math
import platform
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer

DATA = Path(__file__).with_name("data")


def load_data():
    docs, questions = [json.loads((DATA / f"{x}.json").read_text()) for x in ("documents", "questions")]
    validate_data(docs, questions)
    return docs, questions


def validate_data(docs, questions):
    if not docs or not questions:
        raise ValueError("Documents and questions must be nonempty")
    ids = {d["id"] for d in docs}
    if len(ids) != len(docs) or len({q["id"] for q in questions}) != len(questions):
        raise ValueError("Duplicate IDs")
    current = {d["id"] for d in docs if d["status"] == "current"}
    groups = {}
    for q in questions:
        if q["split"] not in {"dev", "test"} or not q["query"].strip():
            raise ValueError("Invalid split or empty query")
        if q["answerable"] != bool(q["gold_ids"]) or not set(q["gold_ids"]) <= current:
            raise ValueError("Invalid gold evidence / answerability")
        if len(set(q["gold_ids"])) != len(q["gold_ids"]):
            raise ValueError("Duplicate gold IDs")
        groups.setdefault(q["group"], set()).add(q["split"])
    if any(len(splits) > 1 for splits in groups.values()):
        raise ValueError("Group leakage between dev and test")


@dataclass(frozen=True)
class Config:
    name: str
    analyzer: str = "word"
    current_only: bool = False
    k: int = 3
    threshold: float = 0.0

    def __post_init__(self):
        if self.analyzer not in {"word", "char"} or self.k < 1 or not 0 <= self.threshold <= 1:
            raise ValueError("Invalid retriever configuration")


class Retriever:
    def __init__(self, docs, config):
        self.config = config
        self.docs = sorted([d for d in docs if not config.current_only or d["status"] == "current"], key=lambda d: d["id"])
        if not self.docs:
            raise ValueError("No indexable documents")
        self.vectorizer = TfidfVectorizer(
            analyzer=config.analyzer, ngram_range=(2, 4) if config.analyzer == "char" else (1, 2),
            sublinear_tf=True, norm="l2")
        # Fit on the frozen searchable corpus only, never on evaluation queries/answers.
        self.matrix = self.vectorizer.fit_transform([d["title"] + " " + d["text"] for d in self.docs])

    def search(self, query):
        scores = (self.matrix @ self.vectorizer.transform([query]).T).toarray().ravel()
        order = sorted((i for i in range(len(scores)) if scores[i] > 0),
                       key=lambda i: (-float(scores[i]), self.docs[i]["id"]))[:self.config.k]
        return [dict(id=self.docs[i]["id"], score=float(scores[i]), status=self.docs[i]["status"],
                     title=self.docs[i]["title"], text=self.docs[i]["text"]) for i in order]


def ranking_metrics(ranked, gold, k):
    """Binary relevance. Duplicates invalid. Unanswerable metrics are undefined, not zero."""
    if k < 1 or len(ranked) != len(set(ranked)):
        raise ValueError("k must be positive; ranked IDs must be unique")
    gold = set(gold)
    if not gold:
        return dict(hit=None, recall=None, mrr=None, ndcg=None)
    rel = [int(doc in gold) for doc in ranked[:k]]
    dcg = sum(r / math.log2(i + 2) for i, r in enumerate(rel))
    ideal = sum(1 / math.log2(i + 2) for i in range(min(k, len(gold))))
    return dict(hit=float(any(rel)), recall=sum(rel) / len(gold),
                mrr=next((1 / (i + 1) for i, r in enumerate(rel) if r), 0.0), ndcg=dcg / ideal)


def evaluate(docs, questions, config):
    retriever = Retriever(docs, config)
    rows = []
    for q in questions:
        hits = retriever.search(q["query"])
        ids = [h["id"] for h in hits]
        accepted = bool(hits and hits[0]["score"] > 0 and hits[0]["score"] >= config.threshold)
        full = q["answerable"] and set(q["gold_ids"]) <= set(ids)
        metrics = ranking_metrics(ids, q["gold_ids"], config.k)
        # This checks retrieval evidence only, NOT factuality of a generated answer.
        error = ("false_accept" if accepted else "correct_abstain") if not q["answerable"] else (
            "missed_answer" if not accepted else "evidence_complete" if full else
            "partial_evidence" if metrics["hit"] else "retrieval_miss")
        rows.append({**q, **metrics, "ranked": hits, "accepted": accepted,
                     "evidence_complete": bool(accepted and full), "error": error,
                     "archive_in_topk": any(h["status"] == "archived" for h in hits)})
    return rows


def mean(values):
    vals = [x for x in values if x is not None]
    return float(np.mean(vals)) if vals else None


def summarize(rows):
    ans = [r for r in rows if r["answerable"]]
    noans = [r for r in rows if not r["answerable"]]
    return dict(n=len(rows), answerable_n=len(ans), unanswerable_n=len(noans),
        **{m: mean(r[m] for r in ans) for m in ("hit", "recall", "mrr", "ndcg")},
        evidence_complete=mean(r["evidence_complete"] for r in ans),
        false_accept=mean(r["accepted"] for r in noans),
        missed_answer=mean(not r["accepted"] for r in ans),
        coverage=mean(r["accepted"] for r in rows),
        archive_in_topk=mean(r["archive_in_topk"] for r in rows))


def select_on_dev(docs, questions):
    if not questions or any(q["split"] != "dev" for q in questions):
        raise ValueError("Tuning accepts dev questions only")
    if not any(q["answerable"] for q in questions) or not any(not q["answerable"] for q in questions):
        raise ValueError("Dev needs answerable and unanswerable cases")
    trials = []
    for analyzer in ("word", "char"):
        for k in (1, 3, 5):
            for threshold in (0.0, 0.15, 0.3, 0.45, 0.6):
                cfg = Config(f"{analyzer}-current-k{k}-t{threshold:g}", analyzer, True, k, threshold)
                s = summarize(evaluate(docs, questions, cfg))
                # Authored teaching utility, not a universal business objective.
                utility = s["evidence_complete"] - s["false_accept"] - 0.25 * s["missed_answer"]
                trials.append(dict(config=asdict(cfg), summary=s, utility=utility))
    best = sorted(trials, key=lambda t: (-t["utility"], t["config"]["k"], -t["config"]["threshold"], t["config"]["name"]))[0]
    return Config(**best["config"]), trials


def paired_group_bootstrap(baseline, candidate, metric="recall", seed=11, n_boot=2000):
    """Resample intent groups, keeping paired systems and paraphrases together."""
    a, b = {r["id"]: r for r in baseline}, {r["id"]: r for r in candidate}
    if a.keys() != b.keys() or len(a) != len(baseline) or len(b) != len(candidate):
        raise ValueError("Paired comparison requires matching unique question IDs")
    group_values = {}
    for key in a:
        if a[key]["group"] != b[key]["group"]:
            raise ValueError("Paired group mismatch")
        if a[key][metric] is not None and b[key][metric] is not None:
            group_values.setdefault(a[key]["group"], []).append(float(b[key][metric])-float(a[key][metric]))
    deltas = np.array([np.mean(x) for x in group_values.values()])
    if len(deltas) < 2 or n_boot < 1:
        raise ValueError("Need at least two comparable groups and positive resamples")
    samples = np.random.default_rng(seed).choice(deltas, size=(n_boot, len(deltas)), replace=True).mean(axis=1)
    lo, hi = np.quantile(samples, [0.025, 0.975])
    return dict(metric=metric, estimand="equal-weight intent-group mean difference",
                delta=float(deltas.mean()), low=float(lo), high=float(hi), groups=len(deltas), seed=seed, n_boot=n_boot)


def release_gate(baseline, candidate, ci):
    """Conservative educational policy; passing does not authorize production release."""
    checks = {
        "false_accept_at_most_10pct": candidate["false_accept"] is not None and candidate["false_accept"] <= 0.1,
        "evidence_complete_at_least_80pct": candidate["evidence_complete"] is not None and candidate["evidence_complete"] >= 0.8,
        "recall_no_observed_drop": candidate["recall"] is not None and baseline["recall"] is not None and candidate["recall"] >= baseline["recall"],
        "recall_ci_lower_at_least_minus_5pp": ci["low"] >= -0.05,
    }
    return {"decision": "REVIEW" if all(checks.values()) else "HOLD", "checks": checks,
            "policy": "teaching-v1; REVIEW still requires human review and online rollout safeguards"}


def run_experiment():
    docs, questions = load_data()
    dev, test = [[q for q in questions if q["split"] == part] for part in ("dev", "test")]
    selected, trials = select_on_dev(docs, dev)
    baseline = Config("word-all-k3", "word", False, 3, 0.0)
    rows = {"baseline": evaluate(docs, test, baseline), "candidate": evaluate(docs, test, selected)}
    summary = {key: summarize(value) for key, value in rows.items()}
    ci = paired_group_bootstrap(rows["baseline"], rows["candidate"])
    manifest = dict(dataset="fictional-shop-v1", evidence="real offline TF-IDF execution on authored synthetic cases",
        generation="none; no LLM was called", python=platform.python_version(), numpy=np.__version__, sklearn=sklearn.__version__,
        seed=11, baseline=asdict(baseline), candidate=asdict(selected),
        data_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DATA.glob("*.json"))},
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        split_ids={part: [q["id"] for q in questions if q["split"] == part] for part in ("dev", "test")})
    run_id = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()[:12]
    return dict(run_id=run_id, manifest=manifest, summary=summary, rows=rows, dev_trials=trials,
                confidence=ci, gate=release_gate(summary["baseline"], summary["candidate"], ci))
