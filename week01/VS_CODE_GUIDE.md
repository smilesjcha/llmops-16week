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

`Tasks: Run Task` → `Week 01: Start and smoke`를 선택한다. VS Code가 서버 시작을 확인한 뒤 합성 고객 피드백을 `demo` 모델 제공자에 보내고 JavaScript 객체 표기법(JavaScript Object Notation, JSON) 응답과 실행 추적을 터미널에 표시한다.

- 서비스 화면: <http://127.0.0.1:8000>
- OpenAPI 명세 문서: <http://127.0.0.1:8000/docs>
- 실행 trace: <http://127.0.0.1:8000/api/v1/traces>
- 운영 지표: <http://127.0.0.1:8000/metrics>

서버 종료는 `Terminal: Terminate Task` → `Week 01: Run TRACE/01`을 선택한다.

## 3. 테스트와 디버깅

- 전체 응용 프로그래밍 인터페이스 테스트: `Testing` 패널 또는 `Tasks: Run Test Task` 실행
- 코드 품질 검사: `Tasks: Run Task` → `Course: Ruff check`
- 서버 중단점 디버깅: `Run and Debug` → `Week 01: Debug TRACE/01`
- 테스트 중단점 디버깅: `Run and Debug` → `Week 01: Debug API tests`

서버 디버깅 중에는 `app/main.py`의 `generate` 함수에 중단점을 두고 UI에서 요청을 보내면 입력 검증, provider 호출, trace 저장 흐름을 순서대로 볼 수 있다.

## 4. 노트북 실습

`week01/lab/week01_trace01_lab.ipynb`를 열고 우측 상단 `Select Kernel` → `Python Environments` → `.venv/bin/python`을 선택한다. 먼저 `Week 01: Run TRACE/01` 작업으로 서버를 실행한 다음 노트북 셀을 위에서 아래로 실행한다.

## 5. Ollama 선택 경로

Ollama는 필수가 아니다. 로컬 모델을 사용할 때만 다음 파일을 만든다.

```bash
cp week01/lab/.env.example week01/lab/.env
ollama serve
ollama pull llama3.2:3b
```

이후 `Week 01: Run TRACE/01 with Ollama .env` 작업 또는 같은 이름의 디버그 구성을 사용한다. `.env`는 Git에서 제외되며 응용 프로그래밍 인터페이스 키나 개인정보를 저장하지 않는다. 실습 입력에도 합성 데이터만 사용한다.

## 문제 해결

- `uv: command not found`: Homebrew에서 `brew install uv` 실행 후 VS Code를 다시 연다.
- 인터프리터 오류: `Environment: Bootstrap`을 다시 실행하고 `.venv/bin/python`을 재선택한다.
- 포트 충돌: 실행 중인 `Week 01: Run TRACE/01` 작업을 종료한 뒤 다시 시작한다.
- Ollama `503`: `ollama serve`와 `ollama list`로 서버와 모델 태그를 확인한다.
