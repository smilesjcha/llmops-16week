# Week 01 · VS Code 실행 가이드

저장소 루트를 Visual Studio Code(VS Code)로 열면 `TRACE/01` 서버, 응용 프로그래밍 인터페이스(Application Programming Interface, API) 테스트, 노트북을 하나의 `.venv`에서 실행할 수 있다. 기준 환경은 **macOS · zsh · uv · CPython 3.11.14**다.

## 1. 최초 환경 준비

1. VS Code에서 `llmops-16week` 저장소 루트를 연다.
2. 추천 확장 프로그램 Python, Pylance, Jupyter, Ruff를 설치한다.
3. Command Palette에서 `Tasks: Run Task` → `Environment: Bootstrap`을 실행한다.
4. 상태 표시줄의 Python 인터프리터가 `.venv/bin/python`인지 확인한다. 다르면 `Python: Select Interpreter`에서 직접 선택한다.

같은 준비를 터미널에서 수행할 때는 다음 명령을 사용한다.

```bash
uv python install 3.11.14
uv venv --python 3.11.14 --allow-existing .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

## 2. 서비스 실행과 확인

실행 횟수를 0부터 직접 기록하려면 `Tasks: Run Task` → `Week 01: Run TRACE/01`을 선택한다. 서버와 자동 요청을 한 번에 확인하려면 `Week 01: Start and smoke`를 사용한다. 후자는 합성 고객 피드백을 `demo` 제공자에 한 번 보내므로 사용자 화면의 전체 실행이 1부터 시작한다.

- 서비스 화면: <http://127.0.0.1:8000>
- OpenAPI 명세 문서: <http://127.0.0.1:8000/docs>
- 실행 trace: <http://127.0.0.1:8000/api/v1/traces>
- 실행 설정: <http://127.0.0.1:8000/api/v1/config>
- 수업용 통계: <http://127.0.0.1:8000/api/v1/stats>
- 운영 지표: <http://127.0.0.1:8000/metrics>

서버 종료는 Command Palette의 `Tasks: Terminate Task` → `Week 01: Run TRACE/01`을 선택한다.

## 3. 테스트와 디버깅

- 전체 응용 프로그래밍 인터페이스 테스트: `Testing` 패널 또는 `Tasks: Run Test Task` 실행
- 코드 품질 검사: `Tasks: Run Task` → `Course: Ruff check`
- 서버 중단점 디버깅: `Run and Debug` → `Week 01: Debug TRACE/01`
- 테스트 중단점 디버깅: `Run and Debug` → `Week 01: Debug API tests`

서버 디버깅 중에는 `app/main.py`의 `generate` 함수에 중단점을 두고 UI에서 요청을 보내면 입력 검증, provider 호출, trace 저장 흐름을 순서대로 볼 수 있다.

## 4. 노트북 실습

`week01/lab/week01_trace01_lab.ipynb`를 열고 우측 상단 `Select Kernel` → `Python Environments` → `.venv/bin/python`을 선택한다. 먼저 `Week 01: Run TRACE/01` 작업으로 서버를 실행한 다음 노트북 셀을 위에서 아래로 실행한다.

## 5. Ollama 빠른 실행 경로

Ollama는 필수가 아니다. `qwen3:4b` 별칭은 현재 Thinking 전용 `qwen3:4b-thinking`과 동일한 모델 ID를 가리키므로, 수업에서는 비추론 모델 `qwen3:4b-instruct`를 사용한다.

```bash
cp week01/lab/.env.example week01/lab/.env
ollama pull qwen3:4b-instruct
ollama list
```

Ollama 애플리케이션이 실행 중이면 `ollama serve`를 다시 실행하지 않는다. 이후 기존 TRACE/01 서버를 종료하고 `Week 01: Run TRACE/01 with Ollama .env` 작업 또는 같은 이름의 디버그 구성을 사용한다.

수업 기본 설정은 다음과 같다.

```text
OLLAMA_MODEL=qwen3:4b-instruct
OLLAMA_THINK=false
OLLAMA_NUM_CTX=2048
OLLAMA_NUM_PREDICT=128
OLLAMA_KEEP_ALIVE=30m
OLLAMA_SEED=42
```

- `OLLAMA_THINK=false`: 비추론 모드를 요청한다.
- `OLLAMA_NUM_CTX`: 입력과 대화 문맥의 토큰 한도다. 긴 문서 실습에서는 늘린다.
- `OLLAMA_NUM_PREDICT`: 한 응답의 최대 생성 토큰 수다.
- `OLLAMA_KEEP_ALIVE`: 모델을 메모리에 유지해 반복 호출의 재적재 시간을 줄인다.
- `OLLAMA_SEED`: 같은 조건을 비교하기 위한 난수 기준값이다.

`--hidethinking`은 생성된 추론 과정을 화면에서 숨길 뿐 생성 자체를 줄이지 않는다. 속도가 목적이면 비추론 모델과 `think:false`를 함께 사용한다. `.env`는 Git에서 제외되며 응용 프로그래밍 인터페이스 키나 개인정보를 저장하지 않는다. 실습 입력에도 합성 데이터만 사용한다.

## 문제 해결

- `uv: command not found`: Homebrew에서 `brew install uv` 실행 후 VS Code를 다시 연다.
- 인터프리터 오류: `Environment: Bootstrap`을 다시 실행하고 `.venv/bin/python`을 재선택한다.
- 포트 충돌: 실행 중인 `Week 01: Run TRACE/01` 작업을 종료한 뒤 다시 시작한다.
- Ollama `503`: `ollama list`에서 `qwen3:4b-instruct` 설치 여부를 확인하고 TRACE/01을 `.env` 작업으로 다시 시작한다.
- Ollama 첫 호출 지연: <http://127.0.0.1:8000/api/v1/config>에서 `Thinking OFF`, 출력 상한, 모델 태그를 확인한다. 이후 호출도 느리면 `ollama ps`에서 CPU·GPU 적재 상태를 확인한다.
- Ollama 추론 문장만 출력: Thinking 전용 모델 별칭 `qwen3:4b`가 선택된 상태다. `.env`의 모델을 `qwen3:4b-instruct`로 바꾼다.
- 노트북 연결 오류: 서버를 먼저 실행하고 커널이 `.venv/bin/python`인지 확인한다.

수업 종료 후 모델 메모리를 바로 비우려면 다음을 실행한다.

```bash
ollama stop qwen3:4b-instruct
```
