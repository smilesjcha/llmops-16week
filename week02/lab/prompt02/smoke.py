"""Offline integration check, optionally against a running localhost server."""

import argparse

import httpx
from fastapi.testclient import TestClient

from .main import app


def main():
    parser = argparse.ArgumentParser(description="PROMPT/02 오프라인 동작 확인")
    parser.add_argument("--url", help="실행 중인 서버 주소, 예: http://127.0.0.1:8002")
    args = parser.parse_args()
    client = httpx.Client(base_url=args.url, timeout=15) if args.url else TestClient(app)
    with client:
        assert client.get("/health").json()["service"] == "PROMPT/02"
        response = client.post(
            "/api/experiments", json={"provider": "demo", "case_ids": ["T01", "T03", "T06"]}
        )
        response.raise_for_status()
        report = response.json()
        assert len(report["rows"]) == 9
        assert report["simulation"] is True
        assert report["summary"]["v3"]["overall_ok"]["passed"] == 3
        assert report["summary"]["v1"]["overall_ok"]["passed"] < 3
        decision = client.post(
            "/api/decisions",
            json={
                "run_id": report["run_id"],
                "version": "v3",
                "reason": "경계 사례 개선을 확인했으며 추가 사례로 재검증할 예정입니다.",
            },
        )
        decision.raise_for_status()
        exported = client.get(f"/api/experiments/{report['run_id']}/export")
        assert exported.json()["decisions"][0]["deployed"] is False
    print("PASS · health, 9 comparable rows, validation, decision, JSON export (offline demo)")


if __name__ == "__main__":
    main()
