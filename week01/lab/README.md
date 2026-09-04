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

## 2. Ollama 선택 경로

```bash
ollama serve
ollama pull llama3.2:3b
```

별도 터미널에서 서비스를 실행한 뒤 사용자 화면의 `OLLAMA · 로컬 모델`을 선택한다. 다른 모델을 사용할 때는 환경 파일을 명시적으로 전달한다.

```bash
cp week01/lab/.env.example week01/lab/.env
# OLLAMA_MODEL을 설치된 모델 태그로 수정
.venv/bin/python -m uvicorn app.main:app --app-dir week01/lab --env-file week01/lab/.env --reload
```

애플리케이션은 `.env`를 암묵적으로 읽지 않는다. `--env-file`을 생략하면 셀 환경변수 또는 기본값 `llama3.2:3b`를 사용한다.

## 3. 40분 실습 루프

1. `demo` 모드에서 같은 입력을 3개 작업 유형으로 실행한다.
2. 실행 추적 식별자, 프롬프트 버전, 응답 지연, 추정 토큰을 비교한다.
3. 온도(temperature)를 바꾸되, 결정론적 데모 모드가 왜 같은 출력을 내는지 설명한다.
4. 가능하면 Ollama로 전환해 실제 생성 결과와 응답 지연을 비교한다.
5. `/api/v1/traces`, `/api/v1/stats`, `/metrics`를 열어 같은 실행의 세 가지 관측 형태를 확인한다.
6. `app/providers.py`의 지시문을 v2로 바꾸고 어떤 지표로 개선을 판단할지 적는다.

## 4. 서비스 계약

| 경로 | 역할 | 첫날 확인할 것 |
|---|---|---|
| `POST /api/v1/generate` | 생성 요청 | 입력 검증, 제공자 교체, 실행 추적 반환 |
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

8000번 포트를 사용할 수 없는 환경에서는 노트북만 다른 주소를 바라보게 할 수 있다.

```bash
TRACE01_BASE_URL=http://127.0.0.1:8765 .venv/bin/python -m jupyter lab
```
