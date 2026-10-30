"""Own ephemeral Uvicorn process; actual TCP streaming and disconnect checks."""

import asyncio
import json
from pathlib import Path
import socket
import subprocess
import sys
import time
import httpx

ROOT = Path(__file__).resolve().parents[1]


async def check(base):
    async with httpx.AsyncClient(base_url=base, timeout=5, trust_env=False) as client:
        for _ in range(100):
            try:
                if (await client.get("/health")).status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            await asyncio.sleep(0.05)
        else:
            raise RuntimeError("own server did not become ready")
        assert (await client.get("/ready")).status_code == 200
        assert (await client.get("/")).status_code == 200
        assert (await client.post("/api/v1/chat", json={"message": "반품 정책"})).status_code == 200
        assert (await client.post("/api/v1/chat", json={"message": "   "})).status_code == 422
        records = []
        for scenario, expected in [("normal", "done"), ("timeout", "error")]:
            start = time.perf_counter()
            first = None
            frames = []
            name = "message"
            async with client.stream(
                "POST", "/api/v1/chat/stream", json={"message": "반품 정책", "scenario": scenario}
            ) as response:
                assert response.status_code == 200
                async for line in response.aiter_lines():
                    if line.startswith("event:"):
                        name = line[6:].strip()
                    if line.startswith("data:"):
                        frames.append(name)
                        if name == "delta" and first is None:
                            first = time.perf_counter() - start
            total = time.perf_counter() - start
            assert frames[-1] == expected
            if expected == "done":
                assert first is not None and first < total
            records.append(
                {
                    "scenario": scenario,
                    "events": frames,
                    "first_delta_ms": None if first is None else first * 1000,
                    "total_ms": total * 1000,
                    "transport": "real localhost TCP; mock character chunks, not tokens",
                }
            )
        async with client.stream("POST", "/api/v1/chat/stream", json={"message": "x"}) as response:
            async for line in response.aiter_lines():
                if line.startswith("event: delta"):
                    break
        for _ in range(100):
            stats = (await client.get("/lab/stats")).json()
            if stats["active"] == 0:
                break
            await asyncio.sleep(0.01)
        assert stats["active"] == 0, "disconnect leaked an active slot"
        out = ROOT / "output/validation/week09-live"
        out.mkdir(parents=True, exist_ok=True)
        receipt = {
            "stream_runs": records,
            "disconnect_active": stats["active"],
            "scope": "local TCP only; no external LLM calls",
        }
        (out / "receipt.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "week09.lab.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--no-access-log",
        ],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        asyncio.run(check(f"http://127.0.0.1:{port}"))
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
