"""Own ephemeral Uvicorn process: real TCP smoke test; no external model calls."""

import asyncio
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


async def check(base):
    async with httpx.AsyncClient(base_url=base, timeout=5, trust_env=False) as c:
        for _ in range(100):
            try:
                if (await c.get("/health/ready")).status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            await asyncio.sleep(0.05)
        else:
            raise RuntimeError("own server failed startup")
        assert (await c.get("/")).status_code == 200
        results = []
        for scenario, expected in [
            ("normal", 200),
            ("retrieval_error", 502),
            ("provider_error", 502),
            ("slow", 504),
            ("normal", 200),
        ]:
            r = await c.post("/api/v1/assist", json={"message": "신청 절차", "scenario": scenario})
            assert r.status_code == expected
            results.append(
                {"scenario": scenario, "status": r.status_code, "trace_id": r.headers["X-Trace-ID"]}
            )
        r = await c.post("/api/v1/assist", json={"message": " "})
        assert r.status_code == 422
        snap = (await c.get("/lab/snapshot")).json()
        assert snap["total"] == 6 and snap["active"] == 0
        assert sum(s["status"] == "ERROR" for s in snap["spans"]) == 6
        metrics = (await c.get("/metrics")).text
        assert "lab_assist_duration_seconds_count 6" in metrics
        normal_id = results[0]["trace_id"]
        normal_spans = sorted(
            [s for s in snap["spans"] if s["trace_id"] == normal_id], key=lambda s: s["offset_ms"]
        )
        from week10.lab.experiments import compare_releases

        receipt = {
            "transport": "actual localhost TCP, synthetic MOCK stages",
            "results": results,
            "normal_spans": normal_spans,
            "snapshot": snap,
            "release_comparison": await compare_releases(),
        }
        out = ROOT / "output/validation/week10"
        out.mkdir(parents=True, exist_ok=True)
        (out / "live-receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
        print(
            json.dumps(
                {
                    "statuses": [x["status"] for x in results],
                    "validation": 422,
                    "active": snap["active"],
                    "total": snap["total"],
                    "scope": receipt["transport"],
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = {
        **os.environ,
        "WEEK10_RELEASE": "v1",
        "WEEK10_LOG_STDOUT": "0",
        "WEEK10_TIMEOUT_S": "0.25",
        "WEEK10_CAPACITY": "2",
    }
    p = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "week10.lab.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--no-access-log",
        ],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    try:
        asyncio.run(check(f"http://127.0.0.1:{port}"))
    finally:
        p.terminate()
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
