# Week 09 · API 실습 실행 가이드

Python 3.11과 저장소의 공통 `requirements.txt`를 사용한다. FastAPI 0.115.14, Pydantic 2.11.7, HTTPX 0.28.1, Uvicorn 0.35.0, NumPy 1.26.4 기준이다. 패키지 추가·버전 변경 없이 실행하며 Redis·Docker·Locust·모델·GPU·API 키는 필수가 아니다.

## 1. VS Code에서 저장소 전체 열기

터미널의 현재 위치가 `llmops-16week`인지 확인한다. 기존 `.venv`가 있다면 재생성하지 않는다.

macOS / Linux:

```bash
# 최초 한 번만
python3.11 -m venv .venv

source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m pytest -q week09/lab/tests
code .
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q week09/lab/tests
code .
```

활성화 정책 문제라면 보안 정책을 바꾸기보다 `.venv\Scripts\python.exe -m pytest -q week09/lab/tests`처럼 해당 Python을 직접 실행한다. VS Code의 Python·Jupyter 확장을 설치한 뒤 Notebook 오른쪽 **Select Kernel → Python Environments → .venv / Python 3.11**을 선택한다.

## 2. Notebook 실행

각 파일은 다른 Notebook이나 실행 중인 서버 없이 독립 실행한다. 위에서 아래로 실행하고, 결과를 예상한 뒤 변수 하나를 바꾸고 다시 실행한다. Jupyter의 최상위 `await`를 사용하므로 셀 안에 `asyncio.run()`을 추가하지 않는다.

| 파일 | 실험 | 권장 | 관련 장표 |
|---|---|---:|---|
| [01 API 계약](notebooks/01_api_contract.ipynb) | 스키마·200·공백/타입/추가 필드 422·OpenAPI·원문 없는 추적 | 15분 | 12–22 |
| [02 비동기·복구](notebooks/02_async_reliability.ipynb) | 순차/동시 대기·스레드 경계·503·504·502·429·취소 해제 | 20분 | 24–35 |
| [03 캐시·버전](notebooks/03_cache_versions.ipynb) | 적중·키 변경·가짜 시계 만료·LRU·콜드 중복·실패 우회 | 15분 | 37–43 |
| [04 스트리밍](notebooks/04_streaming_failures.ipynb) | 프레임·done·error·생성기 종료·TCP 측정 구분 | 15분 | 50–56 |
| [05 부하·프로젝트](notebooks/05_load_and_project.ipynb) | 동시성1/2/6·성공 지연·오류율·처리량·캐시·Ollama 모의 오류·요구사항 | 20분 | 63–79 |

총 111셀 / 코드 53셀. 100분 수업에서는 01 정상·422, 02 용량·시간 초과, 03 캐시 적중·중복, 04 done·error, 05 결과 해석을 선택해 약40분간 실행한다. 전체 85분 분량은 복습에서 확장한다.

이 경로는 `httpx.ASGITransport`로 앱을 직접 호출한다. 실제 네트워크·포트·Uvicorn 처리량을 측정하지 않으며, 특히 스트림 첫 조각 시간을 이 전송 계층에서 측정하지 않는다. 앱은 실행 중에 소스 파일이나 requirements를 덮어쓰지 않는다.

## 3. 브라우저에서 같은 서비스 실행

별도 터미널에서 가상환경을 활성화한 뒤:

```bash
python -m uvicorn week09.lab.app:app --host 127.0.0.1 --port 8009
```

브라우저에서 [실습 화면](http://127.0.0.1:8009/)을 연다.

1. [상태 확인](http://127.0.0.1:8009/health): `status=alive`.
2. [준비 확인](http://127.0.0.1:8009/ready): MOCK의 `ready=true`.
3. 같은 질문을 ‘일반 응답’으로 두 번 실행: 처음 `cached=false`, 다음 `true`.
4. 입력을 공백으로 바꾸어 422 확인 후 정상 입력 복원.
5. ‘제한시간 초과’ 선택: 504와 `deadline_exceeded` 확인.
6. ‘상류 응답 오류’ 선택: 502 확인.
7. ‘정상’ 복원 후 스트리밍: `complete=true`와 `done` 확인.
8. 스트리밍 중 ‘수신 중단’: 미완료 상태와 [최근 메타데이터](http://127.0.0.1:8009/lab/stats)의 `active=0` 확인. 너무 빨리 끝나면 서버 설정 `mock_delay_s`와 `timeout_s`를 함께 늘린 새 앱으로 실험한다.
9. [OpenAPI 문서](http://127.0.0.1:8009/docs)에서 요청 명세·정상·잘못된 입력 확인.
10. 서버 터미널에서 **Ctrl+C**로 종료.

포트가 사용 중이면 다른 프로세스를 종료하지 말고 `--port 8019`로 바꾼다. 주소도 동일하게 바꾼다. 커널 안에 서버를 띄우거나 `--workers`를 늘리지 않는다. 상태·캐시·버킷은 단일 프로세스 메모리다.

이 서버는 인증이 없는 교육용 앱이고 장애 주입을 제공한다. `0.0.0.0`, 터널·공유 링크·공용 서버로 공개하지 않는다.

## 4. 실제 TCP 스트리밍 자동 점검

```bash
python scripts/verify_week09_live.py
```

자신이 만든 임시 Uvicorn 프로세스와 임시 로컬 포트를 사용하고 종료한다. 정상 스트림의 첫 내용 조각·전체 완료, 시간 초과의 오류 이벤트, 클라이언트 단절 후 자원 해제를 확인한다. MOCK 문자 조각이므로 실제 LLM의 TTFT·토큰/초 측정이 아니다.

## 5. 결과와 실험 조건

05의 결과는 로컬 `output/validation/week09-lab/benchmark-report.json`에 저장한다. 성공 지연은 **200 응답만**, 오류율은 **전체 요청**을 분모로 계산한다. 전체 완료 요청/s와 성공 요청/s를 따로 보고한다. 성공 표본이 없으면 분위수는 `None`이다. NumPy의 linear 보간을 사용한다.

- 각 조건24건, 동시 요청1·2·6, 처리 용량2, 캐시 OFF, MOCK 대기30ms.
- 워밍업2건은 집계에서 제외한다.
- 동시성6에서503이 늘면 전체 평균이 낮아질 수 있다. 성공 p95·오류율·성공 처리량을 함께 해석한다.
- 별도 캐시 실험은 워밍업 후 같은 질문을 재사용한다. 모델 추론 최적화 성과가 아니다.
- 작은 표본의 p99로 장기 SLO(Service Level Objective, 서비스 수준 목표)나 운영 보장을 주장하지 않는다.
- 폐쇄형 부하이며 고정 도착률·GPU·실제 모델 품질·장시간 안정성은 측정하지 않는다.
- 로컬 시험은 최대100요청·동시성8이다. 타인의 서버·외부 API를 무단 시험하지 않는다.

## 6. 선택: Ollama 연결

공통 MOCK 경로를 먼저 완료한다. 실제 모델 설치·다운로드를 자동 실행하지 않는다. 터미널에서 `ollama list`와 `curl http://127.0.0.1:11434/api/tags`로 서버·정확한 태그를 확인한다.

MOCK 서버를 Ctrl+C로 종료하고 새 터미널에서:

```bash
source .venv/bin/activate
export WEEK09_PROVIDER=ollama
export WEEK09_MODEL="설치된_정확한_모델_태그"
python -m uvicorn week09.lab.app:app --host 127.0.0.1 --port 8009
```

Windows에서는 `$env:WEEK09_PROVIDER="ollama"`, `$env:WEEK09_MODEL="실제_태그"`를 사용한다. 예시 문자열을 그대로 쓰지 않는다. `/ready`는 설치 목록 검사만 하며 실제 생성 성공을 보장하지 않는다. 앱은 `/api/chat`, `stream:false`, `think:false`, `temperature:0`, `num_predict`와30초 제한을 사용한다. 모델·Ollama 버전에 따라 thinking 지원과 실제 동작은 별도 확인한다. 실제 모델의 속도·품질은 이 초안의 검증 범위가 아니다.

- 연결 불가:503 `provider_unavailable`.
- 상류404:502 `model_not_found`; 모델명 외에 API 경로·서버 버전도 확인.
- 기타 상류 오류:502; 시간 초과:504.
- 실제 Ollama 스트리밍은 이번 앱에서 미지원이며409를 반환한다.
- MOCK 복원: 해당 터미널 종료 후 환경변수 없는 새 터미널에서 실행하거나 `unset WEEK09_PROVIDER WEEK09_MODEL`.

## 7. 합리적인 확장 미션

기본 기능을 복제하기보다 한 가지를 선택해 성공·실패 시험과 함께 개선한다. 별도 필수 과제나 제출 기한을 추가하는 의미는 아니다.

1. 같은 콜드 키의 동시 요청2건이 provider를2회 호출하는 반례에서 시작해 진행 작업 병합을 구현한다. 실패·취소 시 대기자 처리도 정의한다.
2. 자신의 프로젝트 입력·출력 모델을 추가하고 정상·빈 입력·잘못된 타입·허용하지 않는 필드 시험을 만든다.
3. 인증된 사용자·문서 권한을 가진 캐시의 경계를 설계한다. 임의 `userId`를 보내는 것만으로 인증을 구현했다고 쓰지 않는다.
4. 스트림의 ‘200+error’를 HTTP 성공으로만 집계하는 문제를 찾아 완료 기준 지표를 설계한다.

## 8. 구현 파일과 한계

- `app.py`: 라우팅·요청 ID·안전한 오류·브라우저 화면.
- `service.py`: 입력/출력·한도·TTL/LRU·모의/선택 제공자·스트림·자원 해제.
- `benchmark.py`: 제한된 폐쇄형 부하와 지표 정의.
- `tests/test_service.py`: 계약·실패·취소·캐시·스트림·모의 Ollama 검사.

운영 배포 전에는 인증·권한, 전체 본문 바이트 제한, 암호화, 영속 저장, 다중 worker 상태 공유, 중복 실행·제공자 취소, 중앙 지표·보존 정책을 추가 검증해야 한다. 해시는 암호화가 아니며 캐시는 답변을 메모리에 보유한다. 개인정보·학생 원문은 입력하거나 공개 GitHub에 올리지 않는다.
