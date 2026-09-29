"""Generate actual synthetic-corpus measurements for editable teaching charts."""

import argparse
import json
import sys
from pathlib import Path
from time import perf_counter

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from course_labs.retrieval import evaluate, load_cases, retrieve  # noqa: E402

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output-dir", type=Path, default=root / "output" / "validation")
out = parser.parse_args().output_dir
out.mkdir(parents=True, exist_ok=True)
dev = [c for c in load_cases() if c["split"] == "dev"]
configs = [
    {"method": "bm25"},
    {"method": "bm25", "expand": True},
    {"method": "tfidf"},
    {"method": "rrf"},
]
results = [{**config, **evaluate(dev, **config)["summary"]} for config in configs]
(out / "retrieval-chart-data.json").write_text(json.dumps(results, indent=2))
retrieve("상품 반품 기간")  # Warm-up; timings remain local illustrations, not a benchmark.
timings = []
for _ in range(20):
    start = perf_counter()
    retrieve("상품 반품 기간")
    timings.append((perf_counter() - start) * 1000)
(out / "retrieval-timing.json").write_text(json.dumps(timings, indent=2))
print("Generated synthetic dev-set measurements and 20 local timings.")
