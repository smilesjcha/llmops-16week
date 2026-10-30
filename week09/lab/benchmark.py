"""Bounded closed-loop client experiment; not GPU or Internet performance."""

import asyncio
import math
import time
from collections import Counter
import numpy as np


def summarize(rows: list[dict], wall_s: float) -> dict:
    if not rows or not math.isfinite(wall_s) or wall_s <= 0:
        raise ValueError("nonempty rows and positive wall time required")
    good = [r["elapsed_ms"] for r in rows if r["status"] == 200]
    return {
        "n": len(rows),
        "success": len(good),
        "status_counts": dict(Counter(str(r["status"]) for r in rows)),
        "error_rate": 1 - len(good) / len(rows),
        "wall_s": wall_s,
        "completed_rps": len(rows) / wall_s,
        "successful_rps": len(good) / wall_s,
        "success_latency_ms": {
            f"p{p}": float(np.percentile(good, p, method="linear")) if good else None
            for p in (50, 95, 99)
        },
        "scope": "closed-loop bounded concurrency; successful-request latency only",
    }


async def run_load(client, n=12, concurrency=2, use_cache=False, message="API 계약", warmup=2):
    if not 1 <= n <= 100 or not 1 <= concurrency <= 8 or not 0 <= warmup <= 5:
        raise ValueError("local lab bound exceeded: n<=100, concurrency<=8, warmup<=5")
    for _ in range(warmup):
        response = await client.post(
            "/api/v1/chat", json={"message": message, "use_cache": use_cache}
        )
        response.raise_for_status()
    sem = asyncio.Semaphore(concurrency)

    async def one(i):
        async with sem:
            started = time.perf_counter()
            try:
                response = await client.post(
                    "/api/v1/chat", json={"message": message, "use_cache": use_cache}
                )
                status = response.status_code
            except Exception as exc:
                import httpx

                if not isinstance(exc, httpx.HTTPError):
                    raise
                status = "transport_error"
            return {
                "index": i,
                "status": status,
                "elapsed_ms": (time.perf_counter() - started) * 1000,
            }

    start = time.perf_counter()
    rows = await asyncio.gather(*(one(i) for i in range(n)))
    return {"rows": rows, "summary": summarize(rows, time.perf_counter() - start)}
