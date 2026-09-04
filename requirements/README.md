# Python 3.11 Course Environment

## 결정

- canonical interpreter: **CPython 3.11.14**
- support range: `>=3.11,<3.12`
- package install: `uv pip`
- 기본 수업 환경: 저장소 루트 `requirements.txt`
- 충돌 가능성이 큰 RAG, fine-tuning, agent 주차: 별도 virtual environment + 주차 profile

16개 AS-IS notebook은 모두 Python 3.11.9 metadata를 사용한다. 수업용 `uv`가 macOS arm64에 제공하는 같은 minor의 최신 검증 가능 build인 3.11.14로 올리되, 지원 범위는 이후 3.11 security release도 허용한다. NumPy 2.x 및 빠르게 바뀐 LLM framework API를 한꺼번에 올리지 않는 전략이다.

## 설치

```bash
uv python install 3.11.14
uv venv --python 3.11.14 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
python scripts/check_course_materials.py
pytest -q
```

검증된 macOS arm64 transitive lock을 그대로 재현할 때는 다음을 사용한다.

```bash
uv pip install -r requirements/locks/course-base-py311-macos-arm64.txt
```

다른 OS/architecture에서는 root와 해당 주차 source profile을 기준으로 그 플랫폼의 lock을 새로 compile한다. macOS arm64 lock을 Linux나 x86_64에 강제로 재사용하지 않는다.

주차별 격리 환경 예시:

```bash
uv venv --python 3.11.14 .venv-w05
source .venv-w05/bin/activate
uv pip install -r requirements/rag-week05.txt
```

## Profile 지도

| 주차 | 설치 파일 | 상태와 이유 |
|---:|---|---|
| 01 | `requirements.txt` | TRACE/01 + Jupyter + API test |
| 02 | `requirements.txt` | OpenAI/Ollama 호출은 선택 |
| 03 | `requirements.txt` + `observability-week03-10.txt` | Langfuse v3 고정 |
| 04 | `rag-week04-legacy.txt` | deprecated `pinecone-client` 재현 전용 |
| 05 | `rag-week05.txt` | `pinecone` 7.x와 HF retrieval stack |
| 06–07 | `finetune-week06-07.txt` | CPU/macOS와 Linux CUDA 실행을 분리해야 함 |
| 08 | 없음 | 실시간 수업 없이 기말 프로젝트 기획서 온라인 제출·평가 |
| 09 | `requirements.txt`; 부하 테스트는 `loadtest-week09.txt` | ASGI/FastAPI stack |
| 10 | `requirements.txt` + `observability-week03-10.txt` | Langfuse v3 고정 |
| 11 | `eval-week11.txt` | 완전 로컬 TF-IDF/evaluation |
| 12 | `agents-week12.txt` | LangChain integration packages를 한 세트로 고정 |
| 13 | `eval-week11.txt`; neural toxicity는 `safety-week13.txt` | 모델 다운로드 없는 heuristic 경로 우선 |
| 14 | `cost-week14.txt` | tiktoken 선택 경로 포함 |
| 15–16 | 프로젝트가 사용한 profile 조합 | Capstone/실시간 온라인 발표 |

## 단일 거대 환경을 만들지 않는 이유

AS-IS 코드는 같은 이름의 라이브러리를 서로 다른 API 세대로 사용한다.

- Week 04는 `pinecone-client` 5.x, Week 05는 `pinecone` 7.x를 사용하며 두 distribution을 동시에 설치하면 안 된다.
- Week 03/10은 Langfuse v3, Week 06/07의 선택 로깅 코드는 더 오래된 v2 API를 사용한다.
- Week 07 DPO 코드는 TRL의 legacy constructor를 사용해 current TRL 1.x와 호환되지 않는다.
- `bitsandbytes`의 backend 기능은 macOS/CPU와 Linux/CUDA에서 다르다.

따라서 root `requirements.txt`는 전 주차의 **공통 spine**이고, 위험한 stack은 주차별 environment로 고정한다. 이것이 설치 성공률·재현성·수업 복구 시간을 모두 개선한다.

## 검증 수준

자동 검증은 비용·credential·model download 없이 실행되는 범위로 제한한다.

- 16개 notebook JSON/metadata와 code-cell syntax 검사
- root dependency install + `pip check`
- TRACE/01 API, UI, validation, privacy-safe trace, stats, metrics
- 각 profile resolver 검사
- 실행 시 외부 상태가 필요한 OpenAI/Ollama/Pinecone/Langfuse와 HF model download는 manual contract test
- GPU fine-tuning은 Linux/CUDA runner의 별도 smoke가 필요

## 알려진 AS-IS 호환성 부채

- Week 02 notebook 2개에는 저장된 `SyntaxError`/`NameError` output이 있다.
- Week 04의 inline `ragas>=0.1.14`는 실제 사용되지 않으면서 `datasets<3`와 resolver conflict를 만들기 때문에 profile에서 제거했다.
- Week 06/07의 `BitsAndBytesConfig` import와 Langfuse v2 호출은 code migration이 필요하다.
- Week 07의 `DPOTrainer`는 model download와 trainer 1-step test 전까지 후보 lock으로 취급한다.
- AS-IS notebook 안의 `pip install -U`/uninstall cell은 수업 환경 안에서 실행하지 않는다.

## 버전 근거

- [Python 3.11 documentation](https://docs.python.org/3.11/)
- [Python 3.11.16 release](https://www.python.org/downloads/release/python-31116/) — upstream 최신 security release; 공식 binary installer가 없어 이 macOS arm64 수업 환경은 `uv` 제공 3.11.14를 검증 기준으로 사용
- [NumPy 1.26.4](https://pypi.org/project/numpy/1.26.4/) — Python 3.11 wheel 제공
- [Requests 2.34.2](https://pypi.org/project/requests/2.34.2/) — 2.32.4 미만의 CVE-2024-47081 영향 버전 제외
- [FastAPI version guidance](https://fastapi.tiangolo.com/deployment/versions/) — Starlette를 직접 pin하지 않음
- [Pinecone Python SDK mapping](https://docs.pinecone.io/reference/sdks/python/overview)
- [Deprecated pinecone-client distribution](https://pypi.org/project/pinecone-client/)
- [TRL 0.11.4 DPOTrainer](https://huggingface.co/docs/trl/v0.11.4/en/dpo_trainer)
- [Current TRL DPOTrainer](https://huggingface.co/docs/trl/main/dpo_trainer)
- [bitsandbytes platform installation](https://huggingface.co/docs/bitsandbytes/installation)
- [Langfuse Python v3 → v4 upgrade path](https://langfuse.com/docs/observability/sdk/upgrade-path/python-v3-to-v4)
