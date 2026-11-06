# 10주차 · 도구와 서비스 기능의 부연 설명

현재80쪽 강의안 기준이다. 도구 이름을 외우기보다 **어떤 문제를 해결하며, 어디에서 결과를 확인하는가**를 설명한다. 수업의 공통 경로는 Notebook6개이고 Docker·Prometheus는 선택 시연이다.

## 수업 시작 때의 설명 · 약1분

> 오늘 만드는 것은 신청 절차를 안내하는 작은 API 서비스입니다. 답변 생성은 고정 문장으로 대신합니다. 학생 여러분은 현재 어떤 버전이 실행되는지, 요청이 어디에서 실패했는지, 오류가 얼마나 발생했는지, 복구 후 무엇을 확인해야 하는지를 실험합니다. 앱 기능, 실행 환경, 관찰 도구가 각각 어떤 역할을 맡는지 구분해봅시다.

## 장표별 핵심 역할

| 장표 | 도구·기능 | 학생에게 설명할 핵심 | 직접 보여줄 근거 |
|---|---|---|---|
| 7–8·70 | FastAPI | 요청을 검증하고 정상 답변 또는 정해진 오류를 반환하는 앱 프레임워크 | `/docs`의 명세, `/api/v1/assist` 응답 |
| 12·70 | 가상환경·Uvicorn | `.venv`는 Python 의존성 분리, Uvicorn은 브라우저 요청을 받는 ASGI 서버 | 선택 커널·터미널·8010포트 |
| 12–17·49 | Docker·Compose | Docker는 컨테이너 실행, Compose는 앱·Prometheus의 설정과 연결 관리 | `compose ps`의 두 서비스 |
| 18–20 | manifest·config_id | 실행 조건 목록과 설정 지문. Git commit·이미지 digest는 별도 버전 근거 | `/release`와 응답의 X-Release |
| 21–24 | Liveness·Readiness·Lifespan | 생존, 요청 수신 준비, 시작·종료 처리를 각각 확인 | Notebook01·05, `/health/live`, `/health/ready` |
| 27·32–36 | 구조화 로그 | 어떤 요청이 언제 어떤 상태로 끝났는지 필드로 조회 | 로그의 request_id·status·release |
| 28–31 | OpenTelemetry | Trace·Metric·Log의 생성·수집·전달을 위한 표준과 도구 모음 | 공식 도식과 실제 구현 범위 비교 |
| 29–30·37–44 | Trace·Span·Context | 요청 전체 흐름, 작업 구간, 작업 간 ID 연결 | 정상·실패 타임라인과 parent_id |
| 46–58 | Prometheus·PromQL | 숫자 지표를 시간별로 수집·저장·조회 | `/metrics`, Targets UP, 누적 건수 Graph |
| 60–64 | 장애 진단·복구 | 상태 코드·실패 단계·원인 가설·조치·재검증의 연결 | 504 Trace와 후속200·active0 |
| 65–67 | Canary·Rollback·배포 검사 | 후보의 노출·중단·복원 판단과 사전 회귀 검사 | Notebook06의 v1/v2 비교·gate |

ASGI는 **Asynchronous Server Gateway Interface**, Python 비동기 웹 앱과 서버의 인터페이스다. API는 **Application Programming Interface**, 응용 프로그래밍 인터페이스다. PromQL은 **Prometheus Query Language**, 시계열 조회 언어다. CLI는 **Command Line Interface**, 명령줄 인터페이스다.

## OpenTelemetry · 28–31쪽에서의 설명

> 서비스가 느려졌다는 문의만으로는 검색이 느린지, 모델 호출이 느린지 알기 어렵습니다. 요청 안의 작업에 이름과 시작·종료 시각을 남기면 어느 구간에 시간이 걸렸는지 볼 수 있습니다. OpenTelemetry는 여러 언어와 서비스에서 이런 관찰 데이터를 공통 방식으로 만들고 전달하도록 돕습니다.

OpenTelemetry의 줄임말은 **OTel**이다. Trace·Metric·Log를 다루는 표준·API·SDK·계측 라이브러리·Collector 등을 포함한다. 데이터의 장기 저장과 사용자용 시각화는 별도의 백엔드·도구가 담당한다. [공식 개요](https://opentelemetry.io/docs/what-is-opentelemetry/)

| 구성 요소 | 쉬운 설명 | 이번 실습 |
|---|---|---|
| 계측 · Instrumentation | 검색·생성 등 작업에서 관찰 데이터를 남기는 코드 | `telemetry.py`로 직접 구현 |
| Trace | 요청 하나에 연결된 전체 실행 흐름 | 메모리 기록·앱 화면에서 확인 |
| Span | Trace 안의 작업 구간·상태·부모 관계 | assist·retrieve·generate·format |
| Context propagation | 호출 경계를 넘어 같은 실행임을 식별하는 ID 전달 | 제한된 traceparent 처리·ContextVar 예시 |
| SDK | Software Development Kit, 표준에 맞게 데이터를 만드는 언어별 구현 | OpenTelemetry SDK 미포함 |
| Exporter | 계측 데이터를 외부 수집·저장 대상으로 전달하는 구성 요소 | OTel Exporter 미포함 |
| OTLP | OpenTelemetry Protocol, 계측 데이터 전송 규약 | OTLP 전송 미포함 |
| Collector | 데이터를 받아 처리한 뒤 백엔드로 전달하는 구성 요소 | Collector 미포함 |

Collector는 수신·처리·전달을 분리하고 배치 전송·재시도·필터링 등을 구성할 수 있다. 작은 시작 구성은 백엔드에 직접 전송할 수도 있어 Collector를 모든 구성에 필수로 그리지는 않는다. [Collector 공식 설명](https://opentelemetry.io/docs/collector/)

**장표31쪽에서 덧붙일 문장:**

> 이 장표는 일반적인 계측·수집·조회 구조입니다. 오늘 공통 실습에서는 첫 단계의 개념을 직접 구현하고 메모리 기록을 조회합니다. 선택 실습에서는 지표를 Prometheus에 연결합니다. OpenTelemetry SDK와 Collector로 연결하는 구성은 다음 확장입니다.

**장표30쪽에서 덧붙일 문장:** 공식 그림은 여러 서비스 사이의 연결이고, 이번 앱은 한 프로세스의 하위 작업을 추적한다. ID 연결 개념은 같지만 분산 시스템의 네트워크 지연·원격 시계·샘플링까지 시험한 것은 아니다.

### 정상·검색 실패·시간 초과의 비교

| 조건 | HTTP | Span에서 볼 결과 | 학생에게 던질 질문 |
|---|---|---|---|
| 정상 | 200 | assist 안의 retrieve·generate·format | 가장 긴 자식 작업은 무엇인가? |
| 검색 오류 주입 | 502 | retrieve ERROR·assist ERROR, generate 없음 | 생성을 시도하지 않은 근거는 무엇인가? |
| 생성 지연 주입 | 504 | retrieve OK·generate ERROR·assist ERROR | 검색 오류와 같은 조치가 필요한가? |

전체 assist 시간에 자식 시간을 다시 더하면 중복 계산이다. request_id·trace_id는 실행을 찾는 단서이며 인증 근거는 아니다. 시간이 짧거나 HTTP200이라는 사실만으로 답변의 내용 기준 통과를 결론내리지 않는다.

## Prometheus · 46–58쪽에서의 설명

> Trace는 요청 하나가 지나간 작업을 봅니다. Prometheus에서는 최근에 요청이 얼마나 늘었고 오류가 어느 정도였는지 숫자의 변화를 봅니다. 앱이 현재 지표를 노출하면 Prometheus가 주기적으로 읽어 시계열로 보관합니다.

Prometheus는 HTTP Pull 방식의 지표 수집, 시계열 저장, PromQL 조회를 제공한다. 이번 구성의 수집 간격은5초이며 수업용 설정이다. [공식 개요](https://prometheus.io/docs/introduction/overview/)

| 개념 | 실습 지표·조회식 | 부연 설명 |
|---|---|---|
| Counter | `lab_assist_requests_total` | 완료 요청 누적값. 서버 재시작 때 초기화 |
| Gauge | `lab_assist_active` | 현재 실행 중인 작업 수. 짧은 작업은 수집 사이에 끝날 수 있음 |
| Histogram | `lab_assist_duration_seconds_bucket` | 경계 이하 누적 건수. 버킷 합산은 중복 집계 |
| Target | `week10-api` | 수집 대상. UP은 /metrics 수집 성공 |
| Label | `status="502"` | 상태별 집계. 고유 요청 ID를 라벨로 넣으면 조합 수 증가 |
| Rate | `rate(...[1m])` | 최근1분 구간의 초당 변화량. 누적 건수와 단위가 다름 |

### 4분 시연 순서

수업 전에 Docker 이미지를 내려받고 앱·Prometheus를 실행해둔다. 설치는 수업 중 공통 경로로 요구하지 않는다.

1. `/metrics`: 숫자가 들어 있는 텍스트를 보여준다. 이 endpoint 자체는 과거 그래프를 저장하지 않는다.
2. `http://127.0.0.1:9090/targets`: week10-api가 UP인지 확인한다. `api:8010`은 컨테이너 내부 서비스 주소다.
3. 새 앱에서 `seed_traffic.py --count 30`: 정상18·검색 오류6·시간 초과6건을 생성한다.
4. `/query`에서 `lab_assist_requests_total{job="week10-api"}`: Table의 상태별 값 확인 후 Graph로 전환한다.
5. `sum(rate(lab_assist_requests_total{job="week10-api"}[1m]))`: 누적값과 요청/초의 단위 차이를 설명한다.

숫자가 아직 없으면 수집 시각·job 필터·서버·Graph 시간 범위를 확인한다. 최소 두 번의 수집 이전에는 rate가 비어 있을 수 있다. 요청0인 창의 빈 값·NaN을 성공100%로 바꾸지 않는다. 기존 요청이 있으면 누적값은18·6·6보다 커진다.

Grafana는 수집된 데이터에 연결해 대시보드를 만드는 별도 도구다. 현재 실습은 **Prometheus 자체 Table·Graph 화면**을 쓰며 Grafana를 설치하지 않는다. 알림 규칙·Alertmanager도 포함하지 않는다.

## Docker·Compose와 앱 서버 · 12–17·49쪽

> Python 가상환경은 패키지를 분리합니다. 컨테이너 이미지는 앱을 실행하는 파일과 의존성을 함께 구성합니다. Docker로 실행한 API와 Python에서 직접 실행한 API는 같은 기능을 제공하지만 각각 별도 프로세스입니다. Compose는 API와 Prometheus를 함께 시작하고 연결하는 설정을 담습니다.

Compose의 services·networks·ports 설정으로 여러 컨테이너의 구성을 정의한다. [공식 설명](https://docs.docker.com/compose/intro/compose-application-model/)

| 역할 | 이번 실습 | 주의할 구분 |
|---|---|---|
| FastAPI | 입력 명세·검증·오류 응답·endpoint | 앱 코드 |
| Uvicorn | TCP 포트에서 웹 요청을 받아 앱 실행 | 웹 서버 프로세스 |
| HTTPX ASGITransport | Notebook 안에서 앱 직접 호출 | 외부 포트·Uvicorn 없이 실행 |
| Dockerfile | Python·패키지·소스·실행 명령 구성 | 이미지 빌드 명세 |
| Docker container | 빌드된 API 또는 Prometheus 실행 | 실행 인스턴스 |
| Compose | 두 서비스의 포트·준비 조건·네트워크 정의 | 여러 컨테이너의 구성 관리 |

**주소 세 가지:** 브라우저의 API는 `127.0.0.1:8010`, 브라우저의 Prometheus는 `127.0.0.1:9090`, Prometheus가 수집하는 내부 API는 `api:8010/metrics`다. Prometheus 컨테이너에서 localhost는 자기 자신을 가리킨다.

## 상태 검사·배포 판단에서의 설명

- **21–24쪽:** liveness200이더라도 의존성이 준비되지 않으면 readiness503일 수 있다. 이때 모든 요청 실패의 조치를 재시작 하나로 통일하지 않는다. 이번 구현은 앱의 검사이며 Kubernetes 클러스터·로드밸런서를 설치하지 않는다.
- **63–64쪽:** 복구는 상태·정상 요청·내용 기준·자원 해제를 확인한다. 같은 버전 재시작과 이전 버전 복원은 목적이 다르다.
- **65쪽:** Canary는 후보를 일부에 노출하고 관찰해 확대·중단하는 개념이다. 이번 실습은 실제 사용자 트래픽 분기 없이 개념만 설명한다.
- **66–67쪽:** v1/v2 모두 HTTP200이어도 내용 기준은4/4와0/4다. 단순 문자열 회귀 검사이며 LLM 전체 품질 평가가 아니다. 배포 gate의 핵심은 실행 가능한 기준과 보류 근거다.

## 학생이 구분해야 할 현재 구현

| 경로 | 실제 실행되는 것 | 이번 경로에 포함하지 않은 것 |
|---|---|---|
| 공통 Notebook | FastAPI 앱·HTTPX·직접 구현 로그/Span/지표·합성 시험 | 외부 모델·Docker·수집 서버 |
| Python 브라우저 | Uvicorn·TCP·실습 UI·/metrics·/lab/snapshot | OpenTelemetry SDK·Collector·Grafana |
| 선택 Compose | API 컨테이너·실제 Prometheus 수집·Table/Graph | 실제 LLM·분산 Trace 백엔드·운영 알림·트래픽 전환 |

공통 Notebook의 메모리 앱과 브라우저 서버는 별도 실행이다. Notebook의 요청 수가 Prometheus에 안 보이는 것은 정상이다. 같은 앱·같은 버전·같은 관찰 구간에서 나온 증거끼리 비교한다.

## 마무리 질문

1. HTTP200인데 내용이 틀렸다면 어떤 검사와 근거가 필요한가?
2. 검색 오류와 생성 시간 초과를 로그·Trace에서 어떻게 구분했는가?
3. 요청 하나의 실패 원인과 전체 요청의 오류 비율은 각각 어디서 보는가?
4. 직접 확인한 결과와 아직 구현하지 않은 범위를 기획서에 어떻게 나눠 기록할 것인가?

실행 명령·OS별 설치·종료는 [통합 실행 가이드](../QUICKSTART.md), 학생의 단계별 설명은 [Notebook6개](../lab/notebooks/)에 있다.
