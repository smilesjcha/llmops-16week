# Week 10 · 배포·관찰·복구 실습

기존 **Python 3.11 공통 `.venv`와 `requirements.txt`**를 사용한다. 새 패키지·GPU·Ollama·API 키·수집 서버 없이 공통 실습을 실행한다. 검색·생성은 고정 문장과 `asyncio.sleep`을 사용하는 **MOCK**이며 실제 LLM의 품질·속도 시험이 아니다.

## VS Code 실행

저장소 전체를 열고 터미널 위치가 `llmops-16week`인지 확인한다. 기존 `.venv`가 있으면 재생성하지 않는다. 처음 설치하는 경우만 `python3.11 -m venv .venv` 후 공통 requirements를 설치한다.

macOS / Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m pytest -q week10/lab/tests
code .
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q week10/lab/tests
code .
```

처음 환경을 만드는 Windows 사용자는 `py -3.11 -m venv .venv`를 먼저 실행한다. 활성화가 안 되면 `.venv\Scripts\python.exe`를 직접 사용한다. VS Code Python·Jupyter 확장 설치 후 **Select Kernel → Python Environments → .venv / Python 3.11**을 선택한다. Jupyter 셀에서는 최상위 `await`를 그대로 쓰고 `asyncio.run()`을 추가하지 않는다.

## 단계별 Notebook

6개 모두 **서로 독립 실행**한다. 102셀·코드 48셀이다. 각 실험은 예상 → 실행 → 확인 → 프로젝트 적용 순서로 읽는다.

| 단계 | 파일 | 배우는 내용 | 전체 권장 |
|---|---|---|---:|
| 1 | [실행 설정과 릴리스](notebooks/01_release_configuration.ipynb) | 설정 검증·manifest·지문·lifespan·준비 상태 | 12분 |
| 2 | [로그와 요청 연결](notebooks/02_logs_correlation.ipynb) | JSON 조회·request_id·trace_id·개인정보 제외·보존 | 12분 |
| 3 | [Span과 context](notebooks/03_traces_and_context.ipynb) | 계층·시간 포함 관계·header·동시 요청 격리 | 15분 |
| 4 | [지표와 관찰 구간](notebooks/04_metrics_and_windows.ipynb) | counter/gauge/histogram·분모·구간 차이·reset | 15분 |
| 5 | [장애와 복구](notebooks/05_incident_and_recovery.ipynb) | 준비 실패·502/504·실패 Span·후속 정상·자원 해제 | 15분 |
| 6 | [배포 전 검증과 기획서](notebooks/06_release_gate_portfolio.ipynb) | HTTP 200·내용 회귀 분리·배포 보류·근거 기록 | 15분 |

전체 약84분이며, 100분 수업 중 실습40분은 각 파일의 핵심 셀만 선택한다. 자세한 배경은 [수업 진행안](../lecture/TEACHING_GUIDE.md)을 따른다. Notebook의 `lab_client`는 FastAPI lifespan을 명시적으로 열고 HTTPX ASGITransport로 호출한다. 실제 TCP·Uvicorn 성능 시험과 구분한다.

## 브라우저 실습

별도 터미널에서 가상환경을 활성화하고:

```bash
python -m uvicorn week10.lab.app:app --host 127.0.0.1 --port 8010 --no-access-log
```

[실습 화면](http://127.0.0.1:8010/)을 연다.

1. 실행 중인 릴리스의 model·prompt/data·config_id 확인.
2. ‘정상 처리’ 실행 → **200·v1·simulated=true** 확인.
3. `assist → retrieve/generate/format`의 부모·자식 관계와 포함된 기간 확인.
4. ‘검색 단계 오류’ → **502**·retrieve ERROR·generate 미실행 확인.
5. ‘제한시간 초과’ → **504**·generate ERROR 확인.
6. ‘정상 처리’ 복원 → **200**, [snapshot](http://127.0.0.1:8010/lab/snapshot)의 **active=0** 확인.
7. [metrics](http://127.0.0.1:8010/metrics)의 상태별 완료 건수·누적 버킷·count·active 확인.
8. [live](http://127.0.0.1:8010/health/live), [ready](http://127.0.0.1:8010/health/ready), [release](http://127.0.0.1:8010/release), [API 명세](http://127.0.0.1:8010/docs) 확인.
9. 터미널 **Ctrl+C** 종료. 재시작하면 로그·지표·Span 모두 초기화된다.

포트가 사용 중이면 `--port 8011`로 바꾸고 주소도 바꾼다. 인증 없는 로컬 교육용 앱이다. 컨테이너 이외의 직접 실행은 `127.0.0.1`에 바인딩한다. 다중 worker·원격 공개·민감한 원문 입력은 공통 실습 범위가 아니다.

## 버전 변경 실험

서버를 종료한 뒤 새 터미널에서:

```bash
source .venv/bin/activate
export WEEK10_RELEASE=v2
python -m uvicorn week10.lab.app:app --host 127.0.0.1 --port 8010 --no-access-log
```

PowerShell은 `$env:WEEK10_RELEASE="v2"`다. v2는 **의도적으로 잘못된 고정 문장**을 내보낸다. HTTP는200이어도 ‘D01·담당자 확인’ fixture를 통과하지 않는다. Notebook06은 v1/v2를 독립 앱으로 비교하고 이 후보를 보류한다. 실제 트래픽 전환·배포 플랫폼 롤백을 수행한 것은 아니다.

복원은 서버 종료 후 `unset WEEK10_RELEASE`(PowerShell `Remove-Item Env:WEEK10_RELEASE`) 또는 `v1` 지정이다. `WEEK10_TIMEOUT_S` 기본0.25초(0.05–2초), `WEEK10_CAPACITY` 기본2(1–8건), `WEEK10_LOG_STDOUT` 기본1(0/1)도 시작 시 검증한다. 이 범위는 실습 장치 설정이며 운영 권장값이 아니다.

## 선택: Docker

**검증 범위:** 로컬 Python·Notebook·실제 TCP·브라우저 경로를 실행했다. 검수 기기의 Docker daemon이 꺼져 있어 **이미지 빌드와 컨테이너 실행은 미검증**이다. Docker 없이 공통 실습을 완료할 수 있다.

Docker daemon이 실행 중인 환경에서 저장소 루트 기준:

```bash
docker build -t llmops-w10:local week10/lab
docker run --rm --name llmops-w10-demo -p 127.0.0.1:8010:8010 -e WEEK10_RELEASE=v1 llmops-w10:local
```

다른 터미널에서 위의 `/release`·`/health/ready`·정상 요청을 확인하고 자신의 컨테이너만 `docker stop llmops-w10-demo`로 종료한다. `Dockerfile`은 non-root UID10001·작은 허용 파일 목록·readiness HEALTHCHECK를 제공한다. `EXPOSE`는 포트 게시 명령이 아니고, HEALTHCHECK는 컨테이너 재시작·트래픽 전환 정책을 자동 구현하지 않는다.

기본 이미지 태그 `python:3.11.14-slim`은 immutable digest 잠금이 아니다. 운영용 배포는 검토한 이미지 digest·빌드 결과·취약점·아키텍처·비밀 관리까지 확인한다. `requirements-runtime.txt`는 선택 컨테이너용 최소 실행 패키지의 정확한 버전 목록이며, 학생 Notebook은 공통 requirements를 사용한다.

## 자동 확인

```bash
python -m pytest -q week10/lab/tests
python scripts/verify_week10_notebooks.py
python scripts/verify_week10_live.py
```

검증 스크립트는 원본 Notebook을 덮어쓰지 않고 결과를 무시되는 `output/validation/`에 저장한다. TCP 스크립트는 **자신이 생성한 임시 로컬 서버만** 종료한다. 변경 후 강의 차트를 갱신하려면 최신 receipt를 검토해 `lecture/assets/measurements.json`과 PPT·PDF를 함께 갱신한다. 날짜·표본·단위를 함께 유지한다.

## 구현 경계와 확장

- `config.py`: 허용 설정·공개 manifest·설정 지문. 코드 commit·이미지 digest와 구분.
- `app.py`: startup/shutdown·readiness·오류·요청 ID·MOCK 단계.
- `telemetry.py`: ContextVar·부모/자식 Span·원문 없는 완료 로그·Prometheus 텍스트.
- `experiments.py`: lifespan client·동일 fixture 비교·counter 구간 차이.
- 보존: 로그200건·Span800개, 누적 counter는 프로세스 수명. 외부 저장·샘플링·인증 미구현.
- 계측은 **교육용 직접 구현**이며 OpenTelemetry SDK·OTLP 형식·Collector·Grafana·Prometheus 서버를 실행한 것이 아니다.
- Trace Context는00버전·00/01 flags의 제한된 입력만 읽는다. tracestate·baggage·샘플링·전파 완전성·원격 시계는 미구현. ID는 인증 근거가 아니다.
- HTTP middleware의 기간은 응답 생성까지다. 클라이언트 전송·외부 모델 계산 완료의 보장이 아니다. 내부499는 취소 표시용이고 표준 응답 코드로 전송하지 않는다.
- Histogram은 **전체 완료 assist 요청**의 기간이며 실패도 포함한다. 프로브·UI·metrics 조회는 분모에서 제외한다. 5xx 비율의 분모에는422가 포함된다.

확장 시에는 한 가지를 선택한다: 공식 OpenTelemetry SDK 어댑터, 실제 제공자 단계, 버전별 평가 fixture, 영속 수집, 인증된 메타데이터 조회. 추가 서버·패키지는 별도 환경에서 검토하고 공통 환경을 덮어쓰지 않는다.
