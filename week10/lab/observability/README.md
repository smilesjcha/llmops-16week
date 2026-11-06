# 선택 확장 · 브라우저와 Prometheus에서 같은 지표 확인

공통 Notebook을 마친 뒤 진행한다. 여기부터는 **VS Code 터미널과 웹 브라우저**를 쓴다. Notebook 셀에서 Docker를 자동 시작하거나 패키지를 설치하지 않는다.

- **Docker:** 앱과 의존성을 이미지로 묶어 컨테이너로 실행.
- **Docker Compose:** 앱과 Prometheus 두 컨테이너의 설정·포트·연결을 함께 관리.
- **Prometheus:** 앱의 `/metrics`를5초마다 읽고 시간별 숫자를 저장·조회.
- **OpenTelemetry:** 앱의 계측과 데이터 전달을 위한 도구 모음. 이 저장소의 Trace·Span은 교육용 직접 구현이며 SDK·Collector는 포함하지 않는다. SDK는 Software Development Kit, 소프트웨어 개발 도구 모음이다.

### 1. 엔진 준비 · 최초 설치는 수업 전

Mac·Windows는 공식 Docker Desktop을 설치·실행하고 Linux는 Docker Engine과 Compose plugin을 준비한다. 이미 Colima를 쓰는 Mac은 기존 환경을 사용한다.

- [Mac 설치](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Windows 설치](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Linux 설치](https://docs.docker.com/engine/install/) · [Compose plugin](https://docs.docker.com/compose/install/linux/)

**터미널 A · 저장소 루트**에서 `docker info`의 Server 정보와 `docker compose version`을 확인한다. CLI는 Command Line Interface, 명령줄 인터페이스다. `docker --version`만으로 엔진의 실행 상태까지 확인한 것은 아니다. Colima context를 명시할 때는 각 명령의 `docker` 뒤에 `--context colima`를 붙인다.

### 2. 앱과 수집 서버 시작

기존8010포트의 Python 서버는 해당 터미널에서 Ctrl+C로 종료한다. 아래는 **터미널 A** 명령이다.

```bash
docker compose -p llmops-week10-demo -f week10/lab/observability/compose.yaml up -d --build
docker compose -p llmops-week10-demo -f week10/lab/observability/compose.yaml ps
```

최초 이미지를 내려받는 동안에는 시간이 걸린다. 앱이 healthy가 된 뒤 Prometheus가 시작된다. 브라우저에서 [수집 대상](http://127.0.0.1:9090/targets)을 열고 `week10-api`의 **UP**을 확인한다. 수집 주소는 컨테이너 서비스 이름인 `api:8010/metrics`다.

### 3. 요청30건 생성

**터미널 B · 저장소 루트**에서 기존 가상환경을 활성화한 뒤 실행한다. Mac/Linux는 `source .venv/bin/activate`, Windows는 `.venv\Scripts\Activate.ps1`이다.

```bash
python week10/lab/observability/seed_traffic.py --count 30
```

정상18·검색 오류6·시간 초과6건의 합성 요청이다. 새 앱에서 이 요청만 실행했다면 누적값도18·6·6이다. 기존 브라우저 요청이나 seed 재실행이 있으면 누적값이 증가한다. Notebook에서 만든5건은 이 서버에 합쳐지지 않는다.

### 4. 수집·누적값·변화율 구분

[Prometheus 조회 화면](http://127.0.0.1:9090/query)의 입력창에 **한 식씩** 넣는다. Python 코드 셀에 넣지 않는다.

```promql
up{job="week10-api"}
```

1이면 `/metrics` 수집 성공. 답변 내용의 정확성을 판정하는 값은 아니다.

```promql
lab_assist_requests_total{job="week10-api"}
```

Table에서 상태별 건수를 읽고 Graph로 바꾼다. 시간 범위를 최근5분으로 설정해 증가 구간을 본다. 두 오류의 건수가 같으면 선이 겹칠 수 있으므로 Table도 확인한다. 다음 수집까지 약5초 기다린다.

```promql
sum(rate(lab_assist_requests_total{job="week10-api"}[1m]))
```

최근1분의 요청/초다. 누적 건수30과 같은 값이 나오는 식이 아니다. 최소 두 번의 수집이 필요하고 트래픽 없는 구간은 빈 값·0이 나올 수 있다. 오류 비율의0/0은 NaN일 수 있으며 성공100%로 처리하지 않는다. 현재 실행 수 Gauge는 짧은 작업이 수집 사이에 끝나면0만 보일 수 있다.

### 5. 종료·문제 해결

```bash
docker compose -p llmops-week10-demo -f week10/lab/observability/compose.yaml down
```

자신이 만든 프로젝트만 정리한다. 실습 시계열은 tmpfs에 저장되어 종료 시 사라지고, 서버 재시작 뒤 counter도 초기화된다. 전역 정리 명령은 필요하지 않다.

| 증상 | 확인 |
|---|---|
| Cannot connect to Docker daemon | Docker Desktop·Colima 실행과 context 확인 |
| port already allocated | 본인이 실행한 Python 서버 종료 또는 QUICKSTART의 대체 포트 사용 |
| Targets DOWN | compose ps·API 준비 상태·`api:8010/metrics` 주소 확인 |
| 조회 결과 없음 | job 필터·실행한 서버·5초 수집 대기·Graph 시간 범위 확인 |
| 브라우저와 Notebook의 건수가 다름 | 각각 별도 앱이므로 정상. 같은 실행의 숫자끼리 비교 |

설정 전체·추가 조회식은 `week10/lab/observability/`와 `week10/QUICKSTART.md`에 있다. Docker 설치가 안 되어도 앞의 공통 실습은 완료할 수 있다.

[통합 실행 가이드](../../QUICKSTART.md) · [전체 실습](../README.md)
