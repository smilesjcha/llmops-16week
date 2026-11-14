"""Reproducible authored teaching datasets. Not production, load-test or model evidence."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from .experiment import DEFAULT, assign

DATA = Path(__file__).with_name("data")
SCENARIOS = {
    "healthy": "개선 근거와 운영 기준 충족",
    "slow": "해결 확인율 상승·응답 지연 악화",
    "srm": "B 사용자 수집 누락",
}


def make_units(n=2400, seed=12):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        uid = f"u-{i:05d}"
        variant = assign(uid)
        error = int(rng.random() < .012)
        received = int(not error and rng.random() < .90)
        resolved = int(received and rng.random() < (.62 if variant == "A" else .73))
        latency = rng.lognormal(np.log(650 if variant == "A" else 800), .22)
        rows.append({"visitor_id": uid, "variant": variant, "experiment_id": DEFAULT.experiment_id,
                     "config_version": DEFAULT.version, "resolved": resolved, "feedback_received": received,
                     "exposed": 1-error, "error": error, "latency_ms": round(latency, 2),
                     "requests": int(rng.integers(1, 5)), "segment": "mobile" if i%3 else "desktop",
                     "day": i%14+1, "source": "authored_synthetic"})
    return pd.DataFrame(rows)


def build_data():
    DATA.mkdir(parents=True, exist_ok=True)
    base = make_units()
    variants = {"healthy": base, "slow": base.copy(), "srm": base.copy()}
    variants["slow"].loc[base.variant == "B", "latency_ms"] *= 2.5
    # Deliberately drop half of B AFTER allocation, like a logging/filtering fault.
    b_ids = base.index[base.variant == "B"][::2]
    variants["srm"] = base.drop(index=b_ids)
    for name, frame in variants.items():
        frame.to_csv(DATA/f"{name}.csv", index=False, float_format="%.2f")
    metadata = {"source": "authored_synthetic", "seed": 12, "generated_users": len(base),
                "unit": "one eligible visitor; first request outcome within 30 minutes",
                "duration_days": 14, "all_outcome_windows_mature": True,
                "notes": "가상의 14일 종료 스냅샷. day는 분석 설명용이며 실제 서비스 기록이 아님. 사용자 비율·성과를 제품 효과로 인용하지 않음.",
                "scenarios": SCENARIOS, "config_version": DEFAULT.version}
    (DATA/"metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
    return variants


def load_units(scenario="slow"):
    if scenario not in SCENARIOS:
        raise ValueError("healthy / slow / srm 중에서 선택하세요.")
    return pd.read_csv(DATA/f"{scenario}.csv")


if __name__ == "__main__":
    print({k: len(v) for k, v in build_data().items()})
