"""Offline or loopback smoke test for EVAL/03."""

import argparse

import httpx
from fastapi.testclient import TestClient

from .main import app


def main():
    parser = argparse.ArgumentParser(description="EVAL/03 동작 확인")
    parser.add_argument("--url", help="실행 중인 서버 주소")
    args = parser.parse_args()
    client = httpx.Client(base_url=args.url, timeout=15) if args.url else TestClient(app)
    with client:
        assert client.get("/health").json()["service"] == "EVAL/03"
        report = client.post("/api/evaluations", json={"split": "dev"}).json()
        assert len(report["rows"]) == 8
        assert report["summary"]["v0.2"]["overall_ok"]["passed"] == 2
        response = client.post(
            "/api/decisions",
            json={
                "run_id": report["run_id"],
                "version": "v0.2",
                "decision": "hold",
                "reason": (
                    "dev 사례의 구조는 통과했지만 근거와 담당자 정보 오류를 "
                    "test 사례에서 확인합니다."
                ),
            },
        )
        response.raise_for_status()
        assert client.get(f"/api/evaluations/{report['run_id']}/export").status_code == 200
    print("PASS · health, dev 4 cases × 2 versions, rubric, decision, JSON export")


if __name__ == "__main__":
    main()
