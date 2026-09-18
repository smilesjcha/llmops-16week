# 3주차 · VS Code 실행 가이드

실습 이름은 `EVAL/03`, 주소는 **http://127.0.0.1:8003**이다. 1·2주차에서 사용한 저장소 루트와 `.venv`를 계속 사용하며, 새 패키지·API 키·Ollama가 필요하지 않다. 실제 실행 검증은 macOS에서 했다.

## 1. 시작 전 확인

VS Code에서 `llmops-16week` 폴더를 연다. `Python: Select Interpreter`에서 이 저장소의 `.venv`를 선택한다.

```bash
git pull
.venv/bin/python --version
uv pip check --python .venv/bin/python
```

처음 설치라면 Python 3.11.14 기준으로 다음을 실행한다.

```bash
uv python install 3.11.14
uv venv --python 3.11.14 .venv
uv pip install --python .venv/bin/python -r requirements.txt
uv pip check --python .venv/bin/python
```

## 2. 서버와 화면

VS Code의 **Terminal → Run Task → Week 03: Run EVAL/03**을 선택하거나 다음 명령을 실행한다.

```bash
.venv/bin/python -m uvicorn eval03.main:app --app-dir week03/lab --host 127.0.0.1 --port 8003
```

`Uvicorn running on http://127.0.0.1:8003`가 보이면 <http://127.0.0.1:8003>을 연다. 서버 터미널은 그대로 두고 새 터미널에서 다음을 실행한다.

```bash
PYTHONPATH=week03/lab .venv/bin/python -m eval03.smoke
PYTHONPATH=week03/lab .venv/bin/python -m pytest week03/lab/tests -q
```

## 3. 화면 실습 순서

1. 사례 묶음에서 `dev · 개선에 쓰는 개발 사례 4건`을 확인하고 **두 버전 평가 실행**을 누른다.
2. v0.1 결과에서 필수 섹션이 왜 없는지, v0.2 결과에서 M02·M03이 왜 실패인지 연다.
3. 사례 묶음을 `test · 최종 확인 사례 2건`으로 바꾸고 같은 평가를 실행한다.
4. 후보 버전·판단·다음 확인 근거를 입력해 **결정 기록 추가**를 누른다. Demo 결과라면 보통 `보류`가 적절하다.
5. **평가 보고서 JSON 내보내기**로 현재 실행·평가 기준·결정 기록을 저장한다.

Demo는 수업을 위한 고정 응답이다. 프롬프트 파일을 바꿔도 결과가 바뀌지 않으며, 실제 모델 성능을 측정하지 않는다.

## 4. 코드 읽기 순서

`data/cases.json` → `data/demo_outputs.json` → `prompts/meeting_minutes_v0.2.md` → `eval03/core.py` → `eval03/experiments.py` 순서로 읽는다. `core.py`의 `evaluate()`에서 구조·사실·근거·실행 항목을 어떤 규칙으로 나누는지 확인한다.

## 5. 오류 복구

| 증상 | 확인 |
|---|---|
| `No module named eval03` | 서버 명령의 `--app-dir week03/lab` 또는 점검 명령의 `PYTHONPATH=week03/lab` 확인 |
| 8003 포트 사용 중 | 이미 실행 중인 서버를 사용하거나 해당 서버 터미널에서 `Ctrl+C` 후 다시 실행 |
| 화면이 이전 상태 | 브라우저 새로고침 후 다시 평가. 서버 메모리 기록은 재시작하면 초기화 |
| JSON 내보내기 404 | 서버 재시작 뒤의 이전 실행 ID일 수 있음. 다시 실행하고 바로 저장 |
| 결과가 기대와 다름 | `data/demo_outputs.json`과 `cases.json`의 고정 수업 사례를 먼저 확인 |

## 6. Windows PowerShell

Windows에서는 VS Code 자동 작업의 macOS 경로 대신 PowerShell을 사용한다. Windows에서 실제 실행 검증은 하지 않았다.

```powershell
uv python install 3.11.14
uv venv --python 3.11.14 .venv
uv pip install --python .\.venv\Scripts\python.exe -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn eval03.main:app --app-dir week03/lab --host 127.0.0.1 --port 8003
```

새 PowerShell에서 점검한다.

```powershell
$env:PYTHONPATH = "week03/lab"
.\.venv\Scripts\python.exe -m eval03.smoke
.\.venv\Scripts\python.exe -m pytest week03/lab/tests -q
```
