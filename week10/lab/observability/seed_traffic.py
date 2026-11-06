"""Generate a small synthetic sequence for LOCAL Week10 Prometheus charts."""

import argparse
import asyncio
from collections import Counter
from ipaddress import ip_address
from urllib.parse import urlparse
import httpx


def loopback_url(value):
    parsed = urlparse(value)
    if (
        parsed.scheme != "http"
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise argparse.ArgumentTypeError("use a plain local http URL without credentials/query")
    try:
        local = parsed.hostname == "localhost" or ip_address(parsed.hostname).is_loopback
    except (ValueError, TypeError):
        local = False
    if not local or parsed.path not in ("", "/"):
        raise argparse.ArgumentTypeError("only localhost or a loopback IP is allowed")
    return value.rstrip("/")


async def run(base, count):
    statuses = Counter()
    async with httpx.AsyncClient(base_url=base, timeout=5, trust_env=False) as client:
        ready = await client.get("/health/ready")
        ready.raise_for_status()
        for i in range(count):
            scenario = ["normal", "normal", "normal", "retrieval_error", "slow"][i % 5]
            response = await client.post(
                "/api/v1/assist", json={"message": "합성 예시 · 신청 절차", "scenario": scenario}
            )
            expected = {"normal": 200, "retrieval_error": 502, "slow": 504}[scenario]
            if response.status_code != expected:
                raise RuntimeError(f"unexpected status {response.status_code}, expected {expected}")
            statuses[response.status_code] += 1
            print(f"{i + 1}/{count} {scenario}: HTTP {response.status_code}", flush=True)
            await asyncio.sleep(0.5)
    print("synthetic results:", dict(statuses))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", type=loopback_url, default="http://127.0.0.1:8010")
    parser.add_argument("--count", type=int, choices=range(5, 61), default=30)
    args = parser.parse_args()
    asyncio.run(run(args.url, args.count))
