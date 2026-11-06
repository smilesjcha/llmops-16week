"""Independent experiments with explicit lifecycle and synthetic fixture checks."""

from contextlib import asynccontextmanager
import httpx
from .app import create_app
from .config import Settings


@asynccontextmanager
async def lab_client(settings=None):
    app = create_app(settings or Settings())
    # ASGITransport does not run lifespan. Make startup/shutdown explicit.
    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://lab"
        ) as client:
            yield app, client


def fixture_check(answer):
    """Only a small regression guard for this fixed synthetic example, not an LLM judge."""
    return "D01" in answer and "담당자 확인" in answer and "무조건 승인" not in answer


def window_delta(before, after):
    if before["instance_id"] != after["instance_id"]:
        raise ValueError("different process instance; do not subtract these snapshots")
    counts = {int(k): int(v) for k, v in after["status_counts"].items()}
    for k, v in before["status_counts"].items():
        counts[int(k)] = counts.get(int(k), 0) - int(v)
    total = after["total"] - before["total"]
    if total < 0 or any(v < 0 for v in counts.values()):
        raise ValueError("counter reset or different process; do not subtract these snapshots")
    server_errors = sum(v for k, v in counts.items() if 500 <= k < 600)
    return {
        "requests": total,
        "5xx": server_errors,
        "error_rate": server_errors / total if total else None,
        "counts": counts,
    }


async def compare_releases():
    rows = []
    for release in ["v1", "v2"]:
        async with lab_client(Settings(release=release)) as (app, client):
            responses = [
                await client.post("/api/v1/assist", json={"message": "신청 절차"}) for _ in range(4)
            ]
            rows.append(
                {
                    "release": release,
                    "requests": len(responses),
                    "http_success": sum(r.status_code == 200 for r in responses),
                    "fixture_pass": sum(fixture_check(r.json()["answer"]) for r in responses),
                    "manifest": app.state.telemetry.manifest,
                }
            )
    return rows
