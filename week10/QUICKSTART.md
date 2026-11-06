# 10주차 · 수업 링크와 사전 실행

## 학생 공유 링크

| 자료 | GitHub / Drive |
|---|---|
| 강의안 PDF | [10주차 학생용 PDF](https://github.com/smilesjcha/llmops-16week/blob/main/output/pdf/10_week10_observable_deployment.pdf) |
| 실습 Notebook | [01–06 파일 목록](https://github.com/smilesjcha/llmops-16week/tree/main/week10/lab/notebooks) |
| 전체 실습·실행 안내 | [week10/lab](https://github.com/smilesjcha/llmops-16week/tree/main/week10/lab) |
| 기획서2차 양식 HTML | [GitHub에서 내려받기](https://github.com/smilesjcha/llmops-16week/blob/main/curriculum/2026-2/web/project-portfolio-week10.html) |
| 10주차 강의 녹화 | [Drive 영상·보기 전용](https://drive.google.com/file/d/1h2TY8oV7t2fH7MKnlNFsaleC7NGy3z6C/view?usp=sharing) |
| 지난주9주차 녹화 | [Drive 영상·보기 전용](https://drive.google.com/file/d/1SmW8c3hZlwVVcrjycZ5svKfz80aScnLg/view?usp=drivesdk) |

HTML은 GitHub 파일 화면에서 **Download raw file**로 내려받아 브라우저로 연다. 입력 후 **작성본 HTML 저장**을 누르고 저장한 파일을 다시 열어 내용이 남아 있는지 확인한다. 인쇄→PDF도 가능하다.

기획서2차는 **2026년11월6일(금) 오늘 제출**, 미제출자는 **늦어도11월7일(토)까지 제출 요청**이다. 아주대AI대학원은LMS, 군산대·창원대 등 별도 수강생은 공지된 이메일을 이용한다. PPT·Word 기반PDF·HTML에서 선택하며 HWP/HWPX는 제외한다. 정확한 시각은 소속별 공지를 확인한다.

## 먼저 이해할 도구의 역할

| 대상 | 역할 | 화면·확인 |
|---|---|---|
| FastAPI 앱 | 합성 검색·생성 요청을 처리하고 지표를 노출 | `127.0.0.1:8010` |
| `/metrics` | 현재 누적 요청 수·기간·실행 수를 보여주는 텍스트 | 앱 endpoint이며 수집 서버 자체가 아님 |
| Docker | 앱과 의존성을 이미지로 묶고 컨테이너로 실행 | `docker info` · `docker compose ps` |
| Docker Compose | API와 Prometheus 두 컨테이너의 연결·포트·설정을 한 파일로 관리 | `observability/compose.yaml` |
| Prometheus | 앱의 `/metrics`를 주기적으로 읽어 시계열로 저장하고 조회·그래프 제공 | `127.0.0.1:9090` |

실습의 흐름은 **요청 실행 → 앱 지표 변경 → Prometheus가5초마다 수집 → 조회 결과 확인**이다. 추적(Trace)은 앱의 요청별 단계, Prometheus 그래프는 시간별 집계다. 두 화면이 답하는 질문을 구분한다.

## 1. VS Code · 공통 환경

이미 저장소를 받았다면 저장소 루트에서 `git pull --ff-only`로 갱신하고 VS Code에서 폴더 전체를 연다.

```bash
# macOS / Linux · 기존 .venv 재사용
source .venv/bin/activate
python -m pip check
python -m pytest -q week10/lab/tests
code .
```

처음이면 Python3.11 설치 후 `python3.11 -m venv .venv`, 활성화, `python -m pip install -r requirements.txt`를 먼저 진행한다. Windows는 `py -3.11 -m venv .venv`, `.venv\Scripts\Activate.ps1`이다.

`code` 명령이 없으면 VS Code에서 **파일 → 폴더 열기**로 저장소를 연다.

VS Code의 Python/Jupyter 확장 설치 후 Notebook 우측 커널을 **.venv / Python3.11**로 지정한다. Notebook01→02→03→04→05→06 순서로 위에서 아래로 실행한다. 6개 파일은 서로 독립이며 서버·Docker를 켜지 않아도 실행된다.

각 파일의 시작 안내와 단계별 **예상 결과·결과 해석**을 읽고 실행한다. `assert`만 있는 셀은 출력 없이 완료되어도 정상이다. Notebook04 마지막에는 Docker/Prometheus, Notebook05 마지막에는 브라우저 장애·복구의 선택 확장이 있다. 선택 확장은 공통 Notebook 실행을 마친 뒤 진행한다. [완료 확인표](lab/README.md#단계별-notebook)와 [교수용 도구 해설](lecture/TOOL_EXPLANATIONS.md)도 함께 참고한다.

## 2. Python 서비스 화면

```bash
python -m uvicorn week10.lab.app:app --host 127.0.0.1 --port 8010 --no-access-log
```

[앱](http://127.0.0.1:8010/)에서 정상→검색 오류→제한시간 초과→정상 순으로 실행한다.200→502→504→200과 Trace·로그·active0을 확인한다. `/release`, `/health/ready`, `/metrics`도 연다.

다음 Docker 경로로 바꾸기 전에는 이 서버를 **Ctrl+C**로 종료한다. 같은8010포트를 동시에 사용하지 않는다.

## 3. Docker 준비 · 최초 한 번

- **Mac:** [공식 Docker Desktop 설치](https://docs.docker.com/desktop/setup/install/mac-install/)에서 Apple Silicon/Intel에 맞게 설치하고 앱을 실행한다.
- **Windows:** [공식 Docker Desktop 설치](https://docs.docker.com/desktop/setup/install/windows-install/)의 WSL2·가상화 요구사항을 따라 설치 후 실행한다.
- **Linux:** [Docker Engine 공식 설치](https://docs.docker.com/engine/install/) 후 [Compose plugin](https://docs.docker.com/compose/install/linux/)을 준비한다.
- **이미 Colima를 쓰는 Mac:** 다른 Docker 환경을 중복 설치하지 않고 `colima start`, `docker --context colima info`를 사용한다. 이 저장소는 특정 가상화 도구를 필수로 요구하지 않는다.

```bash
docker info
docker compose version
```

`docker --version`만 성공하면 CLI 존재만 확인한 것이다. **`docker info`에서 Server 정보가 보여야** 컨테이너를 실행할 수 있다. 회사 기기는 설치·사용 정책을 확인한다. 연결 오류가 나면 Docker Desktop 또는 기존 Colima의 실행 여부·현재context를 확인한다.

## 4. API + Prometheus 함께 실행

저장소 루트에서:

```bash
docker compose -p llmops-week10-demo -f week10/lab/observability/compose.yaml up -d --build
docker compose -p llmops-week10-demo -f week10/lab/observability/compose.yaml ps
```

Colima context를 명시하려면 각 명령에서 `docker` 뒤에 `--context colima`를 넣는다. 최초 실행은 공식 Python·Prometheus 이미지를 내려받고 Python 패키지를 설치하므로 더 오래 걸린다.

- [API 서비스](http://127.0.0.1:8010/): 앞의 Python 실행과 같은 기능.
- [Prometheus 수집 대상](http://127.0.0.1:9090/targets): `week10-api`가 **UP**인지 확인.
- [Prometheus 조회 화면](http://127.0.0.1:9090/query): 아래 조회식을 입력하고 Table 또는 Graph 확인.

컨테이너 사이의 수집 주소는 `api:8010`이다. Prometheus 컨테이너의 `localhost:8010`은 자기 자신을 뜻하므로 쓰지 않는다. 호스트 브라우저는`127.0.0.1`로 접근한다.

## 5. 학생 앞에서 보여줄 실험

가상환경이 활성화된 다른 터미널에서:

```bash
python week10/lab/observability/seed_traffic.py --count 30
```

외부 모델을 호출하지 않는 합성 요청30건을 만들고 정상·검색 오류·시간 초과를 섞는다. 로컬 loopback 주소만 허용하며 최대60건이다. 이것은 화면 확인용 요청으로 운영 부하 시험이 아니다.

Prometheus 조회창에서 순서대로 실행한다.

```promql
up{job="week10-api"}
```

수집 성공이면1. 이는 `/metrics` 수집 가능의 증거이며 답변 품질 보장이 아니다.

```promql
lab_assist_requests_total{job="week10-api"}
```

200·502·504 상태별 누적 건수. 새 컨테이너에서seed30건만 실행하면18·6·6이며, 기존 요청이 있으면 누적값은 달라진다. **Graph**로 바꾸면 시간에 따라 증가하는 선을 볼 수 있다. 요청을 보낸 직후에는 다음 수집까지 최대약5초 기다린다. 서버 재시작 시counter는 초기화된다.

```promql
sum(rate(lab_assist_requests_total{job="week10-api"}[1m]))
```

최근1분 요청/초. 최소2번의 수집이 필요하며 처음에는 빈 결과가 나올 수 있다. [추가 조회식](lab/observability/queries.promql)에 오류 비율·실행 수·기간 분포 예시가 있다. 짧은 작업의active값은5초 수집 사이에 시작·끝나면 놓칠 수 있다.

**수업 설명:** Docker는 실행 환경, Prometheus는 숫자 수집·조회, 앱의Trace는 한 요청의 실패 구간이다. “수집 대상UP·HTTP200·내용 기준 통과”는 각각 다른 검사다.

## 6. 종료와 재실행

```bash
docker compose -p llmops-week10-demo -f week10/lab/observability/compose.yaml down
```

이번 프로젝트의 컨테이너와 네트워크만 정리한다. 전역`docker system prune`은 사용하지 않는다. Prometheus 저장은 실습용tmpfs여서 종료 시 사라진다. 최대보존2시간·5초 수집은 수업 설정이며 운영 권장값이 아니다.

9090·8010이 사용 중이면 `.env`를 만들지 않아도 터미널 환경변수로 변경할 수 있다. macOS/Linux 예:

```bash
WEEK10_APP_PORT=8011 WEEK10_PROMETHEUS_PORT=9091 docker compose -p llmops-week10-demo -f week10/lab/observability/compose.yaml up -d --build
```

화면 주소와seed의`--url http://127.0.0.1:8011`도 바꾼다. 컨테이너 내부 수집 주소`api:8010`은 그대로다. PowerShell은 `$env:WEEK10_APP_PORT="8011"` 방식으로 설정한다.
