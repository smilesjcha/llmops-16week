# Week 01 검증 보고서

검증 기준일: 2026-09-03  
검증 환경: macOS 26.6.2 arm64 · `uv 0.10.7` · CPython 3.11.14

## 결론

1주차 강의안, PowerPoint, `TRACE/01` 서비스, guided lab notebook과 16주 dependency profile은 model download나 외부 credential 없이 실행 가능한 범위에서 통과했다. 외부 LLM·GPU가 필요한 경로는 아래 수동 검증 경계로 분리했다.

## 자동·로컬 검증 결과

| 영역 | 결과 | 확인 내용 |
|---|---|---|
| root 설치 | PASS | macOS arm64 lock 생성, fresh virtualenv에 123 packages 재설치 |
| dependency integrity | PASS | `uv pip check`: incompatible package 0건 |
| dependency profiles | PASS | observability, W04/W05 RAG, fine-tuning, agents, eval, safety, cost, load-test 9개 resolver 통과 |
| static analysis | PASS | repository 전체 `ruff check .` 통과 |
| API tests | PASS | `pytest`: 4/4 통과 |
| notebook 구조 | PASS | AS-IS 16개 + 신규 Week 01 notebook 1개가 유효한 nbformat 4 JSON |
| notebook 실행 | PASS | guided lab code cell 6/6 실행, Ollama 미설치 fallback까지 정상 |
| 실서비스 smoke | PASS | UI, `/health`, 생성 2회, `/stats`, `/metrics` 모두 HTTP 200 |
| data-minimized trace | PASS | 입력 원문은 JSONL에 저장하지 않고 12자리 fingerprint만 기록 |
| PowerPoint 구조 | PASS | 38 slides, 38 speaker notes, 38 `[Sources]` block |
| PowerPoint layout | PASS | `slides_test.py`: overflow 0건, 최종 렌더 38장 육안 확인 |
| PowerPoint portability | PASS | notes·slide XML의 `/Users/...` 절대 경로 0건 |

## 버전 결정

- Python support range는 `>=3.11,<3.12`, 이 저장소의 검증 기준은 `3.11.14`다.
- Python upstream의 최신 3.11 security release는 3.11.16이지만 공식 binary installer가 없고, 검증 시점 `uv`의 macOS arm64 managed download도 제공되지 않았다. 따라서 수업 당일 재현 가능한 3.11.14를 canonical build로 두고 이후 3.11 patch는 지원 범위 안에서 별도 CI 검증한다.
- `requests==2.34.2`를 사용한다. 2.32.4 미만에 영향을 주는 CVE-2024-47081이 수정된 계열이며, 검증 기준일의 PyPI 최신 안정판이다.
- NumPy는 AS-IS notebook 호환성을 위해 1.26.4에 유지한다. 빠르게 변하는 RAG·agent·fine-tuning stack은 root에 합치지 않고 주차별 profile로 격리한다.

`content_fingerprint`는 익명화가 아니라 동일 입력 비교용 식별자다. 개인정보나 기밀 원문은 실습 입력으로 사용하지 않는다.

## 알려진 AS-IS 경고

구조 오류는 없지만 보존 원본인 `practice/week02/02_advanced_reasoning.ipynb`의 code cell 20에는 닫히지 않은 문자열 1건이 있다. 원본 상태를 숨기지 않기 위해 자동 수정하지 않고 structural checker가 경고로 보고한다.

## 수동 검증 경계

다음 항목은 비용·credential·대용량 model download·GPU 환경이 필요하므로 기본 smoke에서 실행하지 않는다.

- Ollama model pull과 실제 sampling 비교
- OpenAI, Pinecone, Langfuse credential을 사용하는 외부 호출
- Hugging Face model 다운로드와 1-step SFT/DPO
- Linux/CUDA의 QLoRA와 `bitsandbytes` backend
- 실제 강의장 네트워크에서의 다중 사용자 부하 시험

## 재현 명령

```bash
uv python install 3.11.14
uv venv --python 3.11.14 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip check --python .venv/bin/python
ruff check .
pytest -q
python scripts/check_course_materials.py
```

버전 근거: [Python 3.11.16](https://www.python.org/downloads/release/python-31116/), [Requests 2.34.2](https://pypi.org/project/requests/2.34.2/), [Requests release history](https://github.com/psf/requests/blob/main/HISTORY.md).
