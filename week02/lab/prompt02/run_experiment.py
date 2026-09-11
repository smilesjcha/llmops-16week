"""CLI: PYTHONPATH=week02/lab python -m prompt02.run_experiment --provider demo."""

import argparse
import asyncio
import json
from pathlib import Path

from .contracts import ExperimentRequest
from .experiments import run_experiment


def main():
    parser = argparse.ArgumentParser(description="PROMPT/02 비교 실험")
    parser.add_argument("--provider", choices=["demo", "ollama"], default="demo")
    parser.add_argument("--cases", nargs="+", help="예: T01 T03 T06")
    parser.add_argument("--output", type=Path, help="JSON 결과 저장 경로 (생략하면 저장하지 않음)")
    args = parser.parse_args()
    request = ExperimentRequest(provider=args.provider, case_ids=args.cases)
    report = asyncio.run(run_experiment(request))
    print(f"PROMPT/02 | {args.provider} | simulation={report['simulation']}")
    print(f"dataset_hash={report['dataset_hash']}")
    for version, metrics in report["summary"].items():
        print(
            version,
            " ".join(
                f"{key}={metrics[key]['passed']}/{metrics['total']}"
                for key in ("format_ok", "routing_ok", "promise_ok", "review_ok", "overall_ok")
            ),
        )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation prevents accidentally overwriting a previous experiment.
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2, allow_nan=False)
        print(f"Saved: {args.output.resolve()}")
    if any(row["error"] for row in report["rows"]):
        print(next(row["error"] for row in report["rows"] if row["error"]))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
