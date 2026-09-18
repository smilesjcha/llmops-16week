# Week 03 · 실습 검증 기록

검증일: 2026-09-18 · macOS · CPython 3.11.14

| 항목 | 명령 | 결과 |
|---|---|---|
| 단위·API 테스트 | `PYTHONPATH=week03/lab .venv/bin/python -m pytest -q week03/lab/tests` | 10 passed |
| 오프라인 동작 점검 | `PYTHONPATH=week03/lab .venv/bin/python -m eval03.smoke` | PASS |
| 정적 검사 | `.venv/bin/python -m ruff check week03` | All checks passed |
| 브라우저 화면 | `http://127.0.0.1:8003/` | dev/test 선택·평가·결정·내보내기 확인 |

검증한 Demo의 고정 결과는 dev에서 v0.1 `0/4`, v0.2 `2/4`, test에서 v0.1 `0/2`, v0.2 `2/2`다. 이 수치는 실제 LLM 평가가 아니라 수업용 fixture의 기대 결과다.

Windows와 Linux에서는 실행 검증하지 않았다. 해당 환경의 명령은 [VS Code 실행 가이드](VS_CODE_GUIDE.md)에 별도로 적었다.
