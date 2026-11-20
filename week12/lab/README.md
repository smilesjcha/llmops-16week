# 12주차 실습 · 온라인 실험의 설계와 배포 판단

**01 → 02 → 03 → 04 → 05** 순서로 진행합니다. 각 Notebook은 독립적으로 실행할 수 있으며 첫 코드 셀부터 위에서 아래로 실행합니다. Markdown 셀의 설명·예상 결과·확인 질문을 읽으세요.

| Notebook | 배울 내용 | 핵심 실행 | 확인 결과 |
|---|---|---:|---|
| [01 가설·고정 배정](notebooks/01_experiment_contract.ipynb) | 실험 계약, 사용자 단위, 안정적인 해시 | 8분 | A 1196 / B 1204, 재방문에도 같은 버전 |
| [02 API·이벤트](notebooks/02_service_events.ipynb) | 실제 API, 중복 방지, 실패, 피드백, 복구 | 12분 | 같은 요청 중복 없음, 변경 재사용 409, 잘못된 입력 422 |
| [03 데이터 신뢰성](notebooks/03_data_quality_srm.ipynb) | SRM, 누락, 분모, 응답자 선택 편향 | 9분 | 정상 p≈0.870, 누락 사례 INVALID |
| [04 효과·배포 판단](notebooks/04_effect_and_release.ipynb) | %p, 구간, 지연 기준, 반복 확인의 함정 | 12분 | slow HOLD, healthy REVIEW, srm INVALID |
| [05 실제 모델·보고서](notebooks/05_ollama_and_report.ipynb) | Ollama A/B 생성, 출력 한계, 보고서 저장 | 10분 / 수업 발췌 6분 | 실제 응답·종료 이유·토큰, HTML 보고서 |

총 114셀, 코드 셀 38개입니다. [38개 코드 셀별 실행·예상 결과·교수 설명](WALKTHROUGH.md) · [브라우저 교수 안내](https://smilesjcha.github.io/llmops-16week/week12/lecture/instructor/#cells) · [공개 보고서](https://smilesjcha.github.io/llmops-16week/week12/lab/sample/report.html) · **[공개 과제](https://smilesjcha.github.io/llmops-16week/week12/assignment/)**

**11월 20일 과제 개정:** [Langfuse 미션 Notebook과 제출 안내](../assignment/README.md)를 사용합니다. 아래 5개 Notebook은 100분 수업 실습입니다.

## VS Code 준비

저장소 폴더를 VS Code로 열고 Python·Jupyter 확장을 설치합니다. 아래 명령은 **저장소 루트** 터미널에서 실행합니다. 기존 `.venv`가 있으면 재사용하며 새로 만들지 않아도 됩니다.

```bash
git pull --ff-only
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/week12-online.txt
python -m pip check
```

Windows에서는 `py -3.11 -m venv .venv`, `.venv\Scripts\Activate.ps1`을 사용합니다. Python 3.11이 설치되어 있어야 합니다. 기존 커널을 선택한 채 설치하면 다른 환경에 패키지가 들어갈 수 있으므로 오른쪽 위 **Select Kernel → Python Environments → 저장소 .venv / Python 3.11**을 확인합니다.

이 주차는 기존 고정 버전 파일 `base.txt`·`api.txt`를 사용합니다. NumPy 1.26.4, pandas 2.2.3, FastAPI 0.115.14, requests 2.34.2를 재사용합니다. Docker·클라우드 계정·유료 API는 필수가 아닙니다. VS Code의 터미널과 Notebook 커널이 같은 `.venv`인지 첫 코드 셀에서 확인합니다.

## 화면으로 시연하는 순서

02번은 서버를 따로 띄우지 않고 `TestClient`로 실제 앱 라우트를 실행합니다. 학생에게 브라우저도 보여주려면 별도 터미널에서 다음 명령을 실행합니다.

```bash
python -m uvicorn week12.lab.service:app --host 127.0.0.1 --port 8012
```

1. [실습 서비스](http://127.0.0.1:8012/)에서 `u-`로 시작하는 실습 ID와 질문 유형을 선택합니다. 처음에는 **정책 템플릿**으로 실행합니다. 이 경로는 LLM 응답이 아닙니다.
2. 요청 후 응답의 `assigned_variant`, `variant`, `request_id`, `latency_ms` (이벤트 표에서는 실제 제공 버전을 `served_variant`로 표시)를 읽습니다. 사용자 ID를 유지한 요청은 같은 버전입니다.
3. 재전송 버튼으로 같은 요청이 중복 집계되지 않는지 확인합니다. 피드백을 남기고 사용자 분모를 확인합니다.
4. [API 이벤트](http://127.0.0.1:8012/api/events), [요약](http://127.0.0.1:8012/api/summary), [지표](http://127.0.0.1:8012/metrics), [Swagger API](http://127.0.0.1:8012/docs)를 확인합니다.
5. 중단 스위치를 끄면 B 사용자에게 A를 제공합니다. 배정 기록은 유지하며 이 상태의 혼합 데이터는 INVALID입니다. 다시 켜도 과거 복구 기록을 지우거나 정상 실험이라고 바꾸지 않습니다.
6. `Ctrl+C`로 서버를 종료합니다. 기본 SQLite 기록은 Git에서 제외한 `week12/lab/reports/events.sqlite3`에 남습니다. Notebook 02는 별도 임시 DB를 사용하므로 웹 시연 기록과 섞이지 않습니다.

`/metrics`는 Prometheus 형식의 **지표 노출 경로**입니다. 이 명령이 Prometheus 서버나 Docker 컨테이너를 띄우는 것은 아닙니다. 별도 수집기·대시보드는 [10주차 Docker·Prometheus 실습](../../week10/lab/README.md)에서 연결합니다. 로컬 조작 API에는 인증을 붙이지 않았으므로 이 수업 서버는 `127.0.0.1`에만 바인딩합니다.

## 실제 Ollama 실행

[Ollama](https://ollama.com/)를 실행한 뒤 수업 전에 모델을 준비합니다.

```bash
ollama pull qwen2.5:1.5b-instruct
ollama list
```

데스크톱 앱이 이미 실행 중이면 추가 `ollama serve`는 필요 없습니다. 앱 없이 실행하는 환경에서는 별도 터미널에서 `ollama serve`를 실행합니다. 05번은 기본 `RUN_OLLAMA=True`로 실제 `/api/chat`을 호출합니다. 모델 준비가 어렵다면 해당 설정을 `False`로 바꾸면 **SKIP**으로 표시하며 실제 생성으로 기록하지 않습니다.

- 짧은 instruct 모델, `think=false`, `num_ctx=1024`, `num_predict=128`, `temperature=0`, 60초 타임아웃입니다.
- 첫 응답은 모델 로딩 시간이 포함됩니다. A/B 한 번의 응답 시간으로 속도 우열을 결론 내리지 않습니다.
- B 출력이 길이 상한에 걸리면 `done_reason=length`를 확인합니다. 더 간결한 프롬프트 또는 상한 조정을 **새 조건**으로 기록하고 정책 정확성·필수 정보·완결성을 다시 확인합니다.
- 작은 모델의 키워드 통과는 정확성의 증명이 아닙니다. 원문을 읽고 검토합니다.
- 연결 실패나 모델 없음은 실제 오류로 안내합니다. 템플릿으로 몰래 대체하지 않습니다.
- [실제 실행 원문](sample/ollama-responses.json)은 교수의 로컬 실행 사례입니다. CSV의 온라인 성과와 인과적으로 연결된 데이터가 아닙니다.

## 분석 보고서 재생성

```bash
python -m week12.lab.report --out week12/lab/reports
```

`week12/lab/reports/report.html`을 브라우저로 엽니다. `slow`는 **HOLD**(p95 초과), `healthy`는 **REVIEW**(사람 검토 대기), `srm`은 **INVALID**(효과 계산 중지)입니다. 작은 로컬 요청 수는 기간·표본·관찰 창이 끝나지 않아 WAIT이며, 합성 종료 데이터와 섞지 않습니다.

합성 데이터는 `python -m week12.lab.simulate`로 재생성할 수 있습니다. 작성된 조건과 난수 시드를 [data/metadata.json](data/metadata.json)에 남겼습니다. Newcombe–Wilson 구간은 독립 사용자·고정 시점의 두 비율 비교용입니다. 순차 검정·장기 인과 효과·다중 비교 보정을 구현했다고 해석하지 않습니다.

## 막힐 때

| 현상 | 확인 |
|---|---|
| `No module named week12` | 저장소 루트를 열고 첫 경로 셀부터 실행 |
| requests / pandas import 실패 | `.venv` 활성화 후 requirements 설치, 커널 선택 |
| 연결 실패 / 503 | Ollama 실행 여부·11434 포트·모델 설치 확인 |
| 모델 없음 / 404 | `ollama list`에서 정확한 모델 태그 확인 |
| 8012 포트 사용 중 | 기존 수업 서버를 확인하고 별도 포트 지정 |
| 요약 WAIT | 적은 로컬 요청은 계획된 14일 실험이 아님 |
| 요약 INVALID | 중단 스위치 기록·혼합 provider·배정/설정 버전 확인 |
| PDF에서 조작 안 됨 | 슬라이더·그림 확대는 HTML 강의안에서 사용 |

[자동 테스트](tests/test_experiment.py)는 데이터 검증·통계 계산·판정·API 계약을 확인합니다. 유지보수자는 `python -m pip install -r requirements/week12-dev.txt` 후 `python -m pytest week12/lab/tests -q`로 다시 실행할 수 있습니다. 학생 실습에는 개발용 프로필을 설치하지 않아도 됩니다.
