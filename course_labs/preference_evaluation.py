"""Numerical DPO and synthetic evaluation fixtures, not student grading."""
from __future__ import annotations

import numpy as np

DIMENSIONS = ("evidence", "format", "useful", "no_excess_refusal")


def sequence_logprob(probabilities: list[float]) -> float:
    """Sum natural log probabilities for completion tokens only."""
    values = np.asarray(probabilities, dtype=float)
    if values.ndim != 1 or not values.size:
        raise ValueError("nonempty 1D token probabilities required")
    if not np.isfinite(values).all() or (values <= 0).any() or (values > 1).any():
        raise ValueError("probabilities must be finite and in (0, 1]")
    return float(np.log(values).sum())


def evaluation_fixtures() -> list[dict]:
    """Twelve authored flag combinations; no model or human assessment results."""
    pairs = [
        ((1, 0, 1, 1), (1, 1, 1, 1)),
        ((1, 1, 1, 1), (1, 1, 1, 1)),
        ((1, 1, 1, 1), (0, 1, 1, 1)),
        ((1, 1, 1, 1), (1, 1, 0, 0)),
        ((0, 1, 1, 1), (0, 1, 1, 1)),
        ((1, 0, 1, 1), (1, 1, 1, 1)),
        ((1, 1, 1, 1), (1, 1, 1, 1)),
        ((1, 1, 1, 1), (1, 0, 1, 1)),
        ((1, 0, 1, 1), (1, 1, 1, 1)),
        ((1, 1, 1, 1), (1, 1, 1, 1)),
        ((0, 1, 1, 1), (1, 1, 1, 1)),
        ((1, 1, 1, 1), (0, 1, 1, 1)),
    ]
    return [
        {"id": f"SYN-{i:02}", "synthetic": True,
         "baseline": dict(zip(DIMENSIONS, baseline)),
         "candidate": dict(zip(DIMENSIONS, candidate))}
        for i, (baseline, candidate) in enumerate(pairs, start=1)
    ]


def _validate_flags(flags: dict) -> None:
    if set(flags) != set(DIMENSIONS):
        raise ValueError("all four dimensions required")
    if any(type(flags[k]) is not int or flags[k] not in (0, 1) for k in DIMENSIONS):
        raise ValueError("fixture flags must be integer 0 or 1")


def fixture_verdict(baseline: dict, candidate: dict) -> str:
    """Teaching-only gate and Pareto rule. Not a general evaluator or grader."""
    _validate_flags(baseline)
    _validate_flags(candidate)
    b_gate = bool(baseline["evidence"] and baseline["format"])
    c_gate = bool(candidate["evidence"] and candidate["format"])
    if not b_gate and not c_gate:
        return "review"
    if b_gate != c_gate:
        return "baseline" if b_gate else "candidate"
    dims = ("useful", "no_excess_refusal")
    if all(candidate[k] == baseline[k] for k in dims):
        return "tie"
    if all(candidate[k] >= baseline[k] for k in dims):
        return "candidate"
    if all(baseline[k] >= candidate[k] for k in dims):
        return "baseline"
    return "review"


def fixture_summary(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("nonempty fixture rows required")
    counts = dict.fromkeys(("candidate", "baseline", "tie", "review"), 0)
    for row in rows:
        if row.get("synthetic") is not True:
            raise ValueError("this teaching helper accepts synthetic fixtures only")
        counts[fixture_verdict(row["baseline"], row["candidate"])] += 1
    rates = {name: {k: sum(r[name][k] for r in rows)/len(rows) for k in DIMENSIONS}
             for name in ("baseline", "candidate")}
    return {"n": len(rows), "counts": counts, "rates": rates,
            "claim": "Authored flags and teaching rule; not measured LLM quality."}
