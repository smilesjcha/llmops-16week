"""Small, privacy-conscious JSONL trace store used throughout the lab."""

from __future__ import annotations

import json
import math
import threading
from collections import Counter, deque
from pathlib import Path

from .schemas import StatsResponse, TraceRecord


class TraceStore:
    def __init__(self, log_path: Path, max_items: int = 500) -> None:
        self.log_path = log_path
        self._items: deque[TraceRecord] = deque(maxlen=max_items)
        self._lock = threading.Lock()

    def append(self, trace: TraceRecord) -> None:
        line = trace.model_dump_json() + "\n"
        with self._lock:
            self._items.append(trace)
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open("a", encoding="utf-8") as stream:
                stream.write(line)

    def latest(self, limit: int = 20) -> list[TraceRecord]:
        with self._lock:
            return list(reversed(self._items))[:limit]

    def stats(self) -> StatsResponse:
        with self._lock:
            items = list(self._items)
        if not items:
            return StatsResponse(
                total_requests=0,
                success_rate=0.0,
                average_latency_ms=0.0,
                p95_latency_ms=0.0,
                estimated_tokens=0,
                providers={},
            )

        latencies = sorted(item.latency_ms for item in items)
        p95_index = max(0, math.ceil(len(latencies) * 0.95) - 1)
        successes = sum(item.status == "ok" for item in items)
        return StatsResponse(
            total_requests=len(items),
            success_rate=round(successes / len(items), 4),
            average_latency_ms=round(sum(latencies) / len(latencies), 2),
            p95_latency_ms=round(latencies[p95_index], 2),
            estimated_tokens=sum(item.input_tokens_est + item.output_tokens_est for item in items),
            providers=dict(Counter(item.provider for item in items)),
        )

    def prometheus_text(self) -> str:
        stats = self.stats()
        return "\n".join(
            [
                "# HELP trace01_requests_total Total requests observed by TRACE/01.",
                "# TYPE trace01_requests_total counter",
                f"trace01_requests_total {stats.total_requests}",
                "# HELP trace01_success_ratio Successful requests divided by total requests.",
                "# TYPE trace01_success_ratio gauge",
                f"trace01_success_ratio {stats.success_rate}",
                "# HELP trace01_latency_p95_ms Observed p95 latency in milliseconds.",
                "# TYPE trace01_latency_p95_ms gauge",
                f"trace01_latency_p95_ms {stats.p95_latency_ms}",
                "",
            ]
        )

    def dump_debug_json(self) -> str:
        """Useful when teaching how a local trace maps to a later platform."""
        return json.dumps(
            [item.model_dump(mode="json") for item in self.latest()],
            ensure_ascii=False,
            indent=2,
        )
