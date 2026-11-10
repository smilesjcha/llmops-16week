"""python -m week11.lab.run_eval [--out PATH] [--enforce-gate]

The default produces learning evidence even for HOLD. --enforce-gate exits 2
for HOLD so a CI job can block a candidate. REVIEW exits 0, not auto-deploy.
"""
import argparse
import json
from pathlib import Path
from .evaluation import run_experiment


def render_report(result):
    template = Path(__file__).with_name("report-template.html").read_text()
    payload = json.dumps(result, ensure_ascii=False).replace("<", "\\u003c")
    return template.replace("__REPORT_DATA__", payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).with_name("reports"))
    parser.add_argument("--enforce-gate", action="store_true")
    args = parser.parse_args()
    result = run_experiment()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    (args.out / "report.html").write_text(render_report(result))
    print(json.dumps({"run_id": result["run_id"], "candidate": result["manifest"]["candidate"],
                      "summary": result["summary"], "gate": result["gate"]}, ensure_ascii=False, indent=2))
    print("Report:", (args.out / "report.html").resolve())
    if args.enforce_gate and result["gate"]["decision"] == "HOLD":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
