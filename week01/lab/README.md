# TRACE/01 — 첫 번째 관측 가능한 거대 언어 모델 서비스

첫 호출을 만드는 데서 끝내지 않고 `입력 → 프롬프트 버전 → 실행 → 실행 추적 → 지표 → 개선`을 한 화면에서 확인하는 1주차 실습이다. 응용 프로그래밍 인터페이스(Application Programming Interface, API) 키 없이 결정론적 `demo` 제공자로 즉시 실행되며, 선택적으로 Ollama 로컬 모델을 연결할 수 있다.

## 1. 실행

저장소 루트에서 Python 3.11 환경을 준비한다.

```bash
uv python install 3.11.14
uv venv --python 3.11.14 --allow-existing .venv
source .venv/bin/activate
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --app-dir week01/lab --reload
```

브라우저에서 <http://127.0.0.1:8000>을 연다. 응용 프로그래밍 인터페이스 계약은 <http://127.0.0.1:8000/docs>, Prometheus 형식 지표는 <http://127.0.0.1:8000/metrics>에서 확인한다.

화면을 확인한 뒤 [실습 가이드 노트북](week01_trace01_lab.ipynb)을 열면 같은 입력 2회 실행, 실행 추적 비교표, Ollama 선택 경로, 마무리 기록까지 순서대로 진행할 수 있다.

## 2. Ollama 빠른 실행 경로

```bash
ollama pull qwen3:4b-instruct
ollama list
cp week01/lab/.env.example week01/lab/.env
```

Ollama 애플리케이션이 실행 중이면 `ollama serve`를 다시 실행할 필요가 없다. 기존 TRACE/01 서버를 종료한 뒤 환경 파일을 명시해서 다시 실행한다.

```bash
.venv/bin/python -m uvicorn app.main:app --app-dir week01/lab --env-file week01/lab/.env --reload
```

애플리케이션은 `.env`를 암묵적으로 읽지 않는다. `--env-file`을 생략하면 셸 환경변수 또는 코드 기본값을 사용한다. 현재 수업 기준은 다음과 같다.

| 설정 | 기본값 | 역할 |
|---|---|---|
| `OLLAMA_MODEL` | `qwen3:4b-instruct` | 추론 전용 태그가 아닌 비추론 4B 모델 |
| `OLLAMA_THINK` | `false` | Ollama Chat API에 `think:false` 전달 |
| `OLLAMA_NUM_CTX` | `2048` | 짧은 수업 입력용 문맥 한도 |
| `OLLAMA_NUM_PREDICT` | `128` | 장황한 생성과 시간 초과를 줄이는 출력 상한 |
| `OLLAMA_KEEP_ALIVE` | `30m` | 반복 호출 사이 모델 재적재 감소 |
| `OLLAMA_SEED` | `42` | 같은 조건의 비교 재현성 보조 |

`qwen3:4b` 별칭은 현재 Ollama 공식 태그에서 `qwen3:4b-thinking`과 동일한 모델 ID를 가리킨다. 이 태그는 `think:false`를 보내도 추론 문장이 응답 본문에 이어질 수 있으므로 수업 기본으로 사용하지 않는다. `--hidethinking`은 추론을 숨길 뿐 생성 시간을 줄이지 않는다.

실행 설정은 <http://127.0.0.1:8000/api/v1/config>에서 확인한다. 사용자 화면에도 모델, Thinking 요청값, 출력 상한, 문맥 한도와 유지 시간이 표시된다. 첫 호출은 모델 적재 시간이 포함되며 이후 호출과 직접 비교하지 않는다.

## 3. 40분 실습 루프

1. `demo` 모드에서 같은 입력을 두 번 실행한다.
2. 동일해야 하는 출력·프롬프트 버전·모델·콘텐츠 지문과 달라지는 실행 추적 식별자·응답 지연을 구분한다.
3. `/api/v1/config`에서 Ollama 모델과 `Thinking OFF`를 확인한다.
4. 가능하면 Ollama로 전환해 비추론 모델의 생성 결과와 첫 호출·반복 호출 지연을 비교한다.
5. `/api/v1/traces`, `/api/v1/stats`, `/metrics`에서 같은 실행을 개별 기록·집계·수집 지표로 나누어 본다.
6. 다음 버전에서 바꿀 변수와 판단 지표를 두 문장으로 기록한다.

## 4. 서비스 계약

| 경로 | 역할 | 첫날 확인할 것 |
|---|---|---|
| `POST /api/v1/generate` | 생성 요청 | 입력 검증, 제공자 교체, 실행 추적 반환 |
| `GET /api/v1/config` | 실행 설정 | Ollama 모델, Thinking 요청값, 문맥·출력 상한, 모델 유지 시간 |
| `GET /api/v1/traces` | 최근 실행 | 원문 없이 콘텐츠 지문과 메타데이터만 저장 |
| `GET /api/v1/stats` | 수업용 집계 | 성공률, 평균·95번째 백분위 응답 지연, 추정 토큰 |
| `GET /metrics` | 운영 연결점 | Prometheus text exposition 형태 |
| `GET /health` | 상태 확인 | 배포·모니터링의 가장 작은 계약 |

문자 수 기반 토큰은 학습용 추정치다. 실제 비용과 맥락 길이 제한을 판단할 때는 사용하는 모델의 토크나이저와 제공자 사용량을 기준으로 한다.

`content_fingerprint`는 동일 입력 여부를 비교하기 위한 축약 SHA-256이며 익명화가 아니다. 사전 대입으로 추측할 수 있는 개인정보·기밀 원문을 실습에 넣지 말고 합성 예시만 사용한다.

## 5. 테스트

```bash
.venv/bin/python -m pytest -q week01/lab/tests
```

테스트는 사용자 화면, 상태 확인, 요청 검증, 실행 추적 생성, 원문 미저장, 통계, Prometheus 지표와 제공자 실패 복구를 검증한다. Ollama 실제 연결은 로컬 상태에 따라 달라지므로 기본 자동 테스트에서 제외한다.

8000번 포트를 사용할 수 없는 환경에서는 서버와 노트북 주소를 함께 바꾼다.

```bash
.venv/bin/python -m uvicorn app.main:app --app-dir week01/lab --port 8765 --reload
TRACE01_BASE_URL=http://127.0.0.1:8765 .venv/bin/python -m jupyter lab
```

## 6. 공식 참고자료

- [Ollama Thinking](https://docs.ollama.com/capabilities/thinking)
- [Ollama Chat API](https://docs.ollama.com/api/chat)
- [Ollama 모델 유지와 컨텍스트 설정](https://docs.ollama.com/faq)
- [Qwen3 태그 목록](https://ollama.com/library/qwen3/tags)
