# 2주차 · VS Code 실행 가이드

1주차에 사용한 저장소와 공통 `.venv`를 그대로 사용합니다. 별도의 프로젝트 폴더나 유료 API 키는 필요하지 않습니다. 실행할 실습은 **PROMPT/02**, 주소는 **http://127.0.0.1:8002**입니다.

아래 기본 명령과 VS Code의 `Week 02` 자동 작업은 macOS/Linux 경로 기준입니다. **Windows에서는 자동 작업 대신 [Windows PowerShell 실행 순서](#6-windows-powershell-실행-순서)를 사용합니다.** 실제 실행 검증은 macOS에서 진행했으며 Linux와 Windows에서는 실행 검증하지 않았습니다.

## 1. 저장소와 환경

VS Code에서 `llmops-16week` 폴더를 엽니다. 터미널의 현재 위치에 `requirements.txt`, `.python-version`, `week01`, `week02`가 보여야 합니다.

```bash
git pull
.venv/bin/python --version
uv pip check --python .venv/bin/python
```

기준 버전은 Python 3.11.14입니다. 기존 `.venv`가 정상이라면 재설치할 필요가 없습니다. `.venv`에 `pip` 모듈이 없을 수 있으므로 위처럼 `uv pip check`를 사용합니다.

처음 설치하는 경우, `uv`를 설치한 뒤 루트에서 다음을 실행합니다.

```bash
uv python install 3.11.14
uv venv --python 3.11.14 .venv
uv pip install --python .venv/bin/python -r requirements.txt
uv pip check --python .venv/bin/python
```

VS Code 명령 팔레트에서 `Python: Select Interpreter`를 열어 이 저장소의 `.venv`를 선택합니다. 노트북에는 VS Code Python·Jupyter 확장이 필요하며 커널도 같은 환경을 선택합니다.

## 2. 실습 서버

macOS/Linux에서는 `Terminal → Run Task`에서 **Week 02: Run PROMPT/02**를 선택합니다. 또는 터미널에 다음 명령을 실행합니다. Windows는 아래 PowerShell 안내를 따릅니다.

```bash
.venv/bin/python -m uvicorn prompt02.main:app --app-dir week02/lab --port 8002
```

“Uvicorn running on http://127.0.0.1:8002”가 나오면 [실습 화면](http://127.0.0.1:8002)을 엽니다. 이 터미널은 서버용이므로 다음 명령은 새 터미널에서 실행합니다.

`Week 02: Start and smoke`는 서버와 오프라인 점검을 묶은 작업입니다. 이미 서버가 있다면 `Week 02: Smoke demo experiment`만 실행합니다.

## 3. 화면을 따라가는 순서

1. **실험 설정**: `Demo`와 합성 문의 8건이 선택됐는지 확인한 뒤 **3개 버전 비교 실행**을 누릅니다.
2. **프롬프트 확인**: v1·v2·v3를 차례로 열고, 모델에 주는 규칙과 고객 문의가 어떻게 구분되는지 읽습니다.
3. **실패 살펴보기**: T01/v1, T03/v2, T08/v2의 결과 버튼을 열어 문의 원문·기대 기준·실제 응답을 비교합니다.
4. **선택 이유 기록**: 다음에 검증할 버전을 고르고, 근거를 15자 이상 입력한 뒤 **결정 기록 추가**를 누릅니다.
5. **파일 저장**: **JSON 보고서 내보내기**를 누르고 내려받은 파일을 VS Code에서 엽니다. 입력·프롬프트의 해시(내용 식별값), 실행 설정, 검사 결과와 선택 이유가 들어 있는지 확인합니다.

demo는 실제 모델이 아니라 고정 응답을 재생합니다. 출력 수치로 실제 성능 향상을 주장하지 않습니다. `prompts/v3.md`를 수정해도 demo 출력은 바뀌지 않으며, 미리보기와 프롬프트 해시가 바뀐 것만 확인할 수 있습니다.

### 실습 결과를 과제로 제출하기

2주차부터 격주 과제를 진행하며 출제 후 일주일 이내에 제출합니다. 이번 [과제 01](ASSIGNMENT_01.md)은 **2026년 9월 18일 이내**에 JSON 보고서와 짧은 분석 PDF를 제출합니다. 별도의 마감 시각은 공지를 확인합니다.

저장한 비교 결과에서 실패 1건을 골라 이유를 설명하고, 버전 선택 근거·새 합성 문의와 기대 기준·교수에게 묻고 싶은 질문을 정리합니다. 새 문의를 실행하지 않았다면 검증 계획으로 표시합니다. Demo만으로 제출할 수 있으며 Ollama는 선택 사항입니다.

제출은 [소속별 LMS·이메일 경로](ASSIGNMENT_01.md#제출-경로와-일정)를 이용합니다. GitHub는 공개 강의자료 저장소이므로 과제 제출용으로 사용하지 않습니다. 이메일 주소는 수업에서 별도 안내하며, 실제 고객 정보나 API 키를 결과 파일에 넣지 않습니다.

## 4. 코드와 노트북

아래 파일을 먼저 읽습니다.

- `week02/lab/prompts/v2.md`: 출력 형식과 업무 규칙.
- `week02/lab/prompts/v3.md`: 규칙에 추가한 소수 예시.
- `week02/lab/data/cases.json`: 평가 문의와 기대 결과·판단 근거.
- `week02/lab/prompt02/contracts.py`: JSON 출력 명세.
- `week02/lab/prompt02/core.py`: 형식 검사와 의미 검사.
- `week02/lab/week02_prompt02_lab.ipynb`: 오프라인 셀 실행 가이드.

노트북 오른쪽 위 커널에서 `.venv`의 Python 3.11.14를 선택한 뒤 위에서부터 셀을 실행합니다. 노트북은 코드 실험 보고서를 `week02/lab/reports/`에 저장합니다. 이 폴더는 Git에 올라가지 않습니다.

## 5. 선택 · 실제 Ollama

Ollama 앱을 켜거나 별도 터미널에서 `ollama serve`를 실행합니다. 이미 실행 중이면 중복 실행하지 않습니다.

```bash
ollama list
ollama pull qwen3:4b-instruct
ollama run qwen3:4b-instruct "한국어로 준비 완료라고만 답하세요."
```

모델이 한 번 응답한 뒤 실습 화면에서 Ollama를 선택합니다. 자동으로 선택된 T01 한 건으로 먼저 비교합니다. `think:false`와 출력 상한을 코드에서 고정해 긴 Thinking 출력을 요청하지 않습니다. 다운로드와 첫 로딩은 별도 시간이 들 수 있습니다.

환경파일을 사용할 때는 `.env.example`을 복사합니다. `cp`는 로컬에서 파일을 복사하는 명령이며 API 키는 필요하지 않습니다.

```bash
cp week02/lab/.env.example week02/lab/.env
```

`Week 02: Run PROMPT/02 with Ollama .env` 작업을 선택합니다. 기본 Run 작업은 `.env`를 자동으로 읽지 않습니다. 같은 8002번 서버가 이미 있으면 먼저 `Ctrl+C`로 종료합니다.

## 오류별 확인

| 증상 | 확인 순서 |
|---|---|
| `No module named prompt02` | 저장소 루트인지 확인. 서버 명령의 `--app-dir week02/lab` 포함 확인 |
| 8002 포트 사용 중 | 이미 연 서버 사용 또는 기존 터미널에서 `Ctrl+C`. 다른 프로세스를 임의 종료하지 않음 |
| Ollama 연결 오류 | Ollama 앱/`ollama serve` 확인. `/health`는 실습 API의 상태이며 Ollama 준비 상태를 의미하지 않음 |
| Ollama 404 | `ollama list`와 `qwen3:4b-instruct` 태그 확인 |
| 35초 시간 초과 | 모델을 먼저 로드하고 문의 1건만 선택. 나머지 문의는 미실행으로 남음 |
| JSON 형식 실패 | 서버 고장이 아닐 수 있음. 원문과 출력 명세 확인. 이후 의미 검사는 미평가 |
| 보고서 404 | 서버 재시작 또는 최근 30개를 넘겨 기록이 사라짐. 다시 실행 후 바로 다운로드 |
| 노트북 import 실패 | 커널과 `.venv` 확인. 첫 환경 셀부터 재실행 |

수업 종료 전 보고서를 저장하고 서버 터미널에서 `Ctrl+C`로 종료합니다.

## 6. Windows PowerShell 실행 순서

이 저장소의 자동 작업은 `.venv/bin/python`과 `/usr/bin/curl` 경로를 사용하므로 Windows에서 `Run Task`로 실행하지 않습니다. 저장소 루트를 VS Code로 열고, 터미널 종류를 PowerShell로 선택합니다. 아래 명령은 Windows용 경로와 문법으로 안내하며, Windows 실제 실행 검증은 아직 진행하지 않았습니다.

1주차의 `.venv`가 있다면 재설치 없이 다음 상태 확인으로 넘어갑니다. 처음 설치하는 경우에만 `uv` 설치 후 다음을 실행합니다.

```powershell
uv python install 3.11.14
uv venv --python 3.11.14 .venv
uv pip install --python .\.venv\Scripts\python.exe -r requirements.txt
```

`Python: Select Interpreter`에서 `.venv\Scripts\python.exe`를 선택합니다. 노트북 커널도 같은 환경을 사용합니다. 이어서 상태를 확인하고 서버를 실행합니다.

```powershell
.\.venv\Scripts\python.exe --version
uv pip check --python .\.venv\Scripts\python.exe
.\.venv\Scripts\python.exe -m uvicorn prompt02.main:app --app-dir week02/lab --host 127.0.0.1 --port 8002
```

브라우저에서 <http://127.0.0.1:8002>를 엽니다. 서버 터미널은 유지하고 **새 PowerShell 터미널**을 열어 점검합니다.

```powershell
$env:PYTHONPATH = "week02/lab"
.\.venv\Scripts\python.exe -m prompt02.smoke --url http://127.0.0.1:8002
.\.venv\Scripts\python.exe -m pytest week02/lab/tests -q
```

선택형 `.env`를 직접 준비한 경우에는 기존 서버를 `Ctrl+C`로 종료하고, 서버 명령 끝에 `--env-file week02/lab/.env`를 추가합니다. 기본 서버 명령은 `.env`를 자동으로 읽지 않습니다. 이후 화면 실습과 종료 순서는 위 안내와 같습니다.
