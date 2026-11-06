"""Student-facing instructions used by the Week10 notebook builder."""

GETTING_STARTED = """
## 시작 전 · 어디에서 무엇을 실행하나요?

1. VS Code에서 `llmops-16week` **폴더 전체**를 연다. 압축을 풀었다면 Notebook 파일만 따로 옮기지 않는다.
2. VS Code의 Python·Jupyter 확장을 설치하고 우측 위 **Select Kernel → Python Environments → .venv / Python 3.11**을 선택한다. 터미널의 가상환경과 Notebook 커널은 별도 선택이다.
3. 아래 **환경 확인 코드 셀부터** `Shift+Enter`로 한 셀씩 실행한다. 이 파일 안에서는 앞에서 만든 변수를 뒤에서 사용한다.
4. 각 단계의 **예상 결과**와 실제 출력을 대조한다. `assert`는 확인 조건이다. 출력이나 오류가 없어도 셀이 완료되면 조건을 통과한 것이다.
5. 셀을 건너뛰어 `NameError`가 나거나 변수를 여러 번 바꿨다면 **Restart Kernel → Run All**로 처음부터 실행한다. 다른 Notebook의 변수는 가져오지 않는다.

처음 환경을 만드는 경우에만 **VS Code 터미널**에서 실행한다. 아래 명령을 Python 코드 셀에 붙여넣지 않는다.

```bash
# macOS / Linux · 저장소 루트
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell은 `py -3.11 -m venv .venv`, `.venv\\Scripts\\Activate.ps1` 순서다. 활성화가 제한된 환경에서는 `.venv\\Scripts\\python.exe -m pip install -r requirements.txt`처럼 가상환경 Python을 직접 실행한다. 이미 준비된 `.venv`는 그대로 쓴다.

**공통 실습의 실행 방식:** `lab_client`가 메모리 안에 FastAPI 앱을 만들고 시작·종료를 관리한다. HTTPX의 ASGITransport가 같은 프로세스에서 요청을 전달하므로 `uvicorn`, Docker, Ollama, API 키가 필요하지 않다. ASGI는 *Asynchronous Server Gateway Interface*, Python 비동기 웹 앱과 서버 사이의 인터페이스다.

Notebook 앱과 브라우저의 `127.0.0.1:8010` 앱은 **서로 다른 실행**이다. Notebook에서 만든 요청 수가 브라우저·Prometheus에 합쳐지지 않는다. 실제 모델 대신 고정 문장과 대기를 쓰므로 외부 비용은 발생하지 않는다. 실행 시간·요청 ID는 매번 달라져도 정상이다.
"""

TROUBLESHOOTING = """
## 막혔을 때의 확인 순서

| 증상 | 확인·해결 |
|---|---|
| 커널 선택 창만 표시 | Python·Jupyter 확장 설치 후 `.venv`의 Python 선택 |
| `ModuleNotFoundError` | 커널 경로 확인 → 해당 `.venv`로 `python -m pip install -r requirements.txt` |
| 환경 확인에서 저장소를 찾지 못함 | 저장소 전체를 열고 원래 `week10/lab/notebooks` 위치에서 실행 |
| `NameError` | 앞 셀 실행 여부 확인 → Restart Kernel → Run All |
| `asyncio.run() cannot be called...` | Jupyter에서는 제공된 최상위 `await`·`async with`를 그대로 사용 |
| 셀에 출력이 없음 | `assert`만 있는 셀은 오류 없이 끝나면 통과. 왼쪽 실행 번호와 완료 표시 확인 |
| 예상한 422·502·503·504 | 입력 오류·검색 오류·준비 실패·시간 초과를 의도적으로 만든 단계인지 확인 |
| 예상과 다른 `AssertionError` | 바로 위 코드·출력 확인. 변경한 값을 복원하고 처음부터 다시 실행. assert를 지워 통과시키지 않음 |
| 실행 시간·ID가 예시와 다름 | 고정값 비교 대신 상태·부모/자식 관계·분모·검증 결과를 비교 |

실습에서 바꾼 내용은 자신의 사본에 기록한다. 공개 저장소에는 학생 정보·원문 질문·실제 키를 올리지 않는다.
"""

BROWSER_WALKTHROUGH = """
## 선택 확장 · 실제 서비스 화면에서 장애·복구 확인

앞의 Notebook 실험을 마친 뒤 진행한다. **VS Code 터미널**을 열고 저장소 루트에서 기존 `.venv`를 활성화한다. Docker 경로의 API가 이미8010포트에서 실행 중이면 그 앱 화면을 사용하고 서버를 중복 실행하지 않는다.

```bash
python -m uvicorn week10.lab.app:app --host 127.0.0.1 --port 8010 --no-access-log
```

1. 웹 브라우저에서 [실습 앱](http://127.0.0.1:8010/)을 연다. 실행 중인 버전이v1인지 확인한다.
2. 정상 처리: HTTP200·simulated=true, retrieve·generate·format의 정상 실행 확인.
3. 검색 단계 오류: HTTP502, retrieve ERROR와 generate 미실행 확인.
4. 제한시간 초과: HTTP504, generate ERROR 확인.
5. 다시 정상 처리: HTTP200 확인. [snapshot](http://127.0.0.1:8010/lab/snapshot)에서 active=0 확인.
6. 요청 ID·Trace ID로 같은 실행의 로그와 Span을 연결한다. [지표 텍스트](http://127.0.0.1:8010/metrics)에서 상태별 누적 건수를 읽는다.
7. 자신의 서버 터미널에서 Ctrl+C로 종료한다. 재시작하면 메모리 로그·지표·Span은 초기화된다.

각 조건의 화면1개와 실패 구간·복구 근거를 기록한다. 이 앱과 Notebook은 별도 실행이므로 건수·ID가 같을 필요는 없다. port already in use이면 자신이 실행한 서버를 확인하거나 `--port 8011`로 바꾸고 브라우저 주소도 변경한다.

Windows PowerShell의 환경 활성화는 `.venv\\Scripts\\Activate.ps1`, Mac/Linux는 `source .venv/bin/activate`다. v2로 변경했던 터미널이라면 서버 시작 전에 v1으로 복원한다. PowerShell은 `$env:WEEK10_RELEASE="v1"`, Mac/Linux는 `export WEEK10_RELEASE=v1`이다.
"""

# Each row matches the corresponding executable section in the builder.
# Expected observations describe the synthetic fixture, not production guarantees.
GUIDES = {
    "01": {
        "core": "1 기본 설정 → 4 앱의 수명주기 → 5 버전 응답",
        "terms": "**manifest**는 실행 버전·설정 목록, **config_id**는 허용된 설정 값의 지문이다. **lifespan**은 앱 시작·종료 처리, **readiness**는 새 요청을 받을 준비 상태다.",
        "steps": [
            ("release=v1, model=mock-fixed-v1, timeout_s=0.25, capacity=2 등이 담긴 사전.", "같은 코드라도 프롬프트·데이터·처리 한도가 다르면 실행 조건이 다르다. 비교 전에 이 목록을 남긴다."),
            ("기본 설정의 manifest는 같고, timeout_s를0.5로 바꾸면 config_id가 달라진다.", "설정 차이를 찾는 식별자다. 코드 변경을 식별하는 Git commit과는 별도로 기록한다."),
            ("ValueError 메시지3개. 이 단계의 오류 메시지는 예상한 출력이다.", "지원하지 않는 버전·숫자가 아닌 제한시간·0인 처리량을 시작 전에 거부한다. 허용 범위를 바꿔 운영 권장값으로 사용하지 않는다."),
            ("컨텍스트 안에서는 live·ready가200, 종료 뒤 started=False·draining=True. assert만 있는 부분은 무출력 통과.", "app 객체 생성만으로 시작 처리가 실행되지는 않는다. lab_client의 async with가 수명주기를 열고 닫는다."),
            ("HTTP200 응답, release=v1, simulated=true. X-Release와 /release의 값이 일치한다.", "학생은 화면의 이름만 보지 않고 실제 처리 버전을 응답에서도 확인한다. ID·실행 시간은 매번 달라진다."),
            ("Dockerfile 본문과 USER 10001 설정.", "파일 읽기만 실행한다. 이미지 빌드·컨테이너 실행은 터미널의 선택 실습이다."),
            ("capacity=1·2인 manifest 두 개와 서로 다른 config_id.", "capacity는 동시에 받아들일 작업 수의 상한이다. 이 셀은 설정 비교이며 처리량 성능 측정은 아니다."),
        ],
        "try": ["timeout_s를0.25와0.5로 비교하고 config_id가 바뀐 이유를 적는다.", "정상 범위의 capacity=1과2를 비교한 뒤 원래 코드로 복원한다.", "실제 프로젝트에서 manifest에 넣을 값3개와 공개하면 안 되는 값1개를 고른다."],
        "record": "어떤 설정이 바뀌었으며, 현재 동작을 어떤 버전·설정으로 재현할 수 있는가?",
    },
    "02": {
        "core": "1 비교 요청 → 2 허용 필드 → 3 오류 조회 → 4 사용자 문의와 연결",
        "terms": "**구조화 로그**는 JSON 필드로 조회하는 이벤트 기록이다. **request_id**는 요청 식별자, **trace_id**는 관련 작업 묶음의 식별자다. **라벨**은 지표를 나눠 집계하는 분류 값이다.",
        "steps": [
            ("정상200·검색 오류502·빈 입력422. 조건을 통과하면 출력 없이 완료된다.", "서버 장애와 입력 검증 실패를 구별할 비교 표본을 만든다. 외부 서버에 요청하는 셀이 아니다."),
            ("로그3건의 JSON. 입력 원문 SYNTHETIC-ONLY는 snapshot에 없다.", "상태·기간·버전·연결 ID로 원인을 좁힐 수 있다. 실습의 허용 필드 목록을 읽는다."),
            ("status>=500인 검색 오류 로그1건.", "422는 사용자 입력 검증 실패라 이 필터에 포함되지 않는다. 어떤 실패를 집계하는지 먼저 정의한다."),
            ("502 응답의 X-Request-ID에 대응하는 로그1건.", "문의의 요청 ID와 로그를 연결한다. ID는 실행을 찾는 단서이며 사용자 인증 수단은 아니다."),
            ("같은 trace_id의 retrieve·assist가 ERROR. generate·format은 없다.", "검색이 실패했으므로 이후 단계를 실행하지 않았다. 전체 실패와 최초 실패 단계를 함께 읽는다."),
            ("유한 상태·경로 상한24, 요청 ID를 곱한 가상 상한240000.", "서로 다른 라벨 조합마다 시계열이 늘어날 수 있다. 계산 예시이며 실제 저장량·비용 측정은 아니다."),
            ("retention의 로그 한도200·Span 한도800과 허용 로그 필드 검사 통과.", "최근 로그 보관 건수와 프로세스 수명 동안의 누적 counter는 서로 다른 범위다."),
        ],
        "try": ["오류 필터를 status>=400으로 바꾸고422가 추가되는지 비교한다.", "502 대신 정상 응답의 request_id로 조회해 로그1건을 찾는다.", "로그에 남길 필드와 지표 라벨로 쓸 필드를 나눠 선택 이유를 적는다."],
        "record": "한 요청의 실패를 원문 없이 어떤 필드 조합으로 찾을 수 있는가?",
    },
    "03": {
        "core": "1 정상 경로 → 2 부모·자식 검증 → 3 시간 해석 → 7 실패 지점",
        "terms": "**Trace**는 한 요청의 실행 흐름, **Span**은 그 안의 작업 구간이다. **parent_id**는 부모 Span 연결 값, **ContextVar**는 동시에 실행되는 작업별 문맥을 분리하는 Python 도구다. **OpenTelemetry(OTel)**는 계측 데이터의 생성·수집·전달을 위한 도구 모음이다. 이 Notebook은 직접 구현한 Span을 사용하고 OTel SDK·Collector를 설치하지 않는다. **W3C**는 World Wide Web Consortium, 웹 표준화 기구다. **OTLP**는 OpenTelemetry Protocol, 계측 데이터 전송 규약이다.",
        "steps": [
            ("assist·retrieve·generate·format의4개 Span과 offset_ms·duration_ms.", "assist가 전체 요청을 감싸고 나머지는 하위 작업이다. 보통 generate가 가장 오래 걸리지만 기기별 시간은 달라진다."),
            ("자식3개의 parent_id가 assist의 span_id와 같고 trace_id도 같다.", "이름이 비슷한 작업을 임의로 묶는 대신 ID 관계로 같은 요청의 실행임을 확인한다."),
            ("부모 기간·자식 합계·가장 긴 자식 작업 이름.", "부모가 자식을 포함한다. 둘을 더하면 같은 시간을 중복 계산한다. 외부 네트워크·GPU 시간은 이 실험에 없다."),
            ("전달한 a32자리 trace_id와 b16자리 원격 parent_id를 유지한다.", "헤더로 이전 작업과 연결하는 제한된 예시다. 전체 W3C 처리나 OpenTelemetry SDK가 구현된 것은 아니다."),
            ("새 trace_id 두 개, parent=None. 잘못된 헤더는 예외 없이 새 문맥으로 시작한다.", "형식이 맞지 않는 ID를 그대로 신뢰하지 않는다. 이 교육용 파서는 지원 범위가 제한적이다."),
            ("동시 요청2개의 trace_id가 서로 다르고 각 Trace에4개 Span. 무출력 통과.", "작업별 문맥을 분리해 다른 요청의 부모 ID가 섞이지 않는지 확인한다."),
            ("retrieve·assist ERROR, generate·format 없음.", "HTTP502와 실행 구간을 함께 보면 검색 단계에서 중단됐음을 알 수 있다. 전체 시간이 길다는 설명보다 원인이 구체적이다."),
        ],
        "try": ["정상·retrieval_error를 번갈아 실행해 생성된 Span 이름을 비교한다.", "시간 값 대신 부모·자식 포함 관계를 설명하는 간단한 도식을 그린다.", "학생 자신의 서비스에 필요한 Span 이름을3개 정의한다. 예: 문서 검색·재정렬·답변 생성."],
        "record": "어느 단계가 실패하거나 느렸으며, 어떤 Trace·Span 관계가 그 판단을 뒷받침하는가?",
    },
    "04": {
        "core": "1 관찰 전 스냅샷 → 2 기간 차이 → 3 텍스트 노출 형식 → 6 트래픽 없는 구간",
        "terms": "**Counter**는 누적 건수, **Gauge**는 현재 값, **Histogram**은 구간별 분포다. **le**는 less than or equal, 해당 경계 이하라는 뜻이다. **SLO**는 Service Level Objective, 서비스 수준 목표다. **PromQL**은 Prometheus Query Language, 시계열 조회 언어다.",
        "steps": [
            ("before.total=0, after.total=5. 정상2·서버 오류2·입력 오류1.", "live·metrics 조회는 assist 요청 분모에 포함하지 않는다. 이 파일에서는 모든 완료 assist 요청을 분모로 쓴다."),
            ("requests=5, 5xx=2, error_rate=0.4. 상태별 건수도 확인한다.", "이 실험의 오류 비율은2/5다. 입력 오류422를 제외하는 정책이라면 분모부터 다시 정의해야 한다."),
            ("counter·gauge·histogram 텍스트. request_id·trace_id 라벨은 없다.", "현재 숫자를 노출하는 endpoint다. 아래 선택 실습에서 실제 Prometheus 서버가 별도로 이 텍스트를 수집한다."),
            ("버킷 값이 순서대로 같거나 증가하고 +Inf 버킷은5.", "같은 요청이 여러 이하 경계에 포함된다. 버킷 값들을 단순 합산해 요청 수로 사용하지 않는다."),
            ("성공 평균과 전체 평균, 각각의 분모2·5.", "빠른 실패가 섞이면 전체 평균이 더 작아질 수 있다. 짧은 응답 시간이 내용 품질이나 성공의 증거가 되지는 않는다."),
            ("같은 snapshot 사이의 error_rate=None, 역순 차이는 ValueError 안내.", "요청0은 관측 부족이다. 재시작·다른 실행의 누적값을 그대로 빼서 비율을 계산하지 않는다."),
            ("관찰한 구간은 ‘원인 확인’, 요청0 구간은 ‘관측 부족’.", "예시 분기 규칙이다. 이 작은 표본의10%를 실제 서비스의 알림 기준으로 그대로 사용하지 않는다."),
        ],
        "try": ["사본의 첫 단계 시나리오 목록에 normal을1개 추가한다. 뒤의 assert도 새 기대값에 맞게 바꾸고 분모6·서버 오류2·오류 비율 약0.333을 확인한다.", "성공만 포함한 분모와 전체 완료 요청 분모의 차이를 문장으로 적는다.", "선택 Docker 실습에서 같은 지표의 누적값과 최근1분 rate를 비교한다."],
        "record": "어떤 시간 구간·대상·실패 정의·분모로 지표를 계산했는가?",
    },
    "05": {
        "core": "1 준비 상태와 생존 상태 → 2 시간 초과의 원인 → 3 실패 Trace 조회 → 4 복구 실험 → 6 상태 복원",
        "terms": "**Liveness**는 프로세스 생존, **Readiness**는 요청 수신 준비 상태다. **Timeout**은 작업의 제한시간, **Mitigation**은 사용자 영향을 줄이는 완화 조치다. **Runbook**은 증상·조치·검증을 정리한 대응 절차다.",
        "steps": [
            ("live200·ready503·새 assist503. 무출력 통과.", "프로세스는 살아 있지만 의존성 fixture가 준비되지 않았다. 새 요청을 받는 판단과 재시작 판단을 구분한다."),
            ("정상200과 지연 조건504. 완료 후 active=0.", "slow는 제한시간보다 긴 대기를 주입한다. 처리 슬롯이 해제되는지까지 확인한다."),
            ("실패한 요청의 retrieve OK·generate ERROR·assist ERROR. format 없음.", "시간 초과가 생성 단계에서 발생했음을 찾는다. 기기별 duration_ms 숫자 자체보다 실패 구간에 집중한다."),
            ("후속 정상 요청200, active=0, 고정 정상 답변.", "앞 요청이 실패한 뒤에도 새 요청을 처리할 수 있는지 확인한다. 새 lab_client 블록은 이전 실험과 별도 앱이다."),
            ("고정 문장+asyncio.sleep, 외부 GPU 취소 미구현·미측정 안내.", "로컬 대기 취소가 실제 모델 서버의 연산 취소를 증명하지 않는다. 운영에서는 제공자의 취소·과금 조건을 별도 검증한다."),
            ("의존성 복원 뒤 ready200·정상 응답·fixture 통과. 무출력 통과.", "상태 검사와 내용 검사까지 재확인해야 복구 근거가 된다. dependency_ok는 교육용 내부 조작이다."),
            ("증상·Trace 근거·가설·완화·재검증·남은 위험을 담은 사전.", "이 예시는 코드가 채운 기록이다. 자신의 관찰 결과로 고쳐 쓰고 미검증 범위를 남긴다."),
        ],
        "try": ["시간 초과504와 검색 오류502에서 실패 Span을 비교한다.", "의존성 복원 전후에 live·ready 상태를 각각 기록한다.", "‘서버 재시작’만 적은 복구 기록에 정상 응답·내용 검사·자원 해제 근거를 보완한다."],
        "record": "증상·근거·가설·조치·재검증을 구분했고, 실제로 복구된 범위는 어디까지인가?",
    },
    "06": {
        "core": "1 릴리스 비교 → 2 HTTP와 내용 기준 → 3 배포 차단 조건 → 6 프로젝트 증거의 계층",
        "terms": "**Fixture**는 재현 가능한 시험 입력·조건, **Regression**은 변경 후 기존 기준의 실패다. **Release gate**는 후보 배포 전 통과 조건이다. **PRD**는 Product Requirements Document, 제품 요구사항 문서다.",
        "steps": [
            ("v1·v2의 결과2행. 각 버전에 합성 입력4건.", "v2는 일부러 잘못된 고정 응답을 반환한다. 모델 우열이 아니라 배포 전 회귀 검사의 필요성을 실험한다."),
            ("HTTP 성공은4·4, 내용 기준 통과는4·0. 비율은 각각1.0/1.0과1.0/0.0.", "서버 응답 성공과 업무 요구사항 충족은 별도 검사다.4건을 전체 정확도로 일반화하지 않는다."),
            ("{'v1': True, 'v2': False}.", "이 fixture에서 내용 회귀가 있는 후보를 보류한다. 실제 프로젝트에는 더 다양한 검수 데이터와 실패 분류가 필요하다."),
            ("v1 manifest 출력과 내용 기준 검사 통과.", "이전 버전을 새 앱으로 확인하는 로컬 비교다. 배포 플랫폼의 실제 사용자 트래픽 전환은 포함하지 않는다."),
            ("문서·담당자 키워드가 있어도 ‘무조건 승인’이 있는 문장은 거부.", "특정 문자열 규칙은 작은 회귀 방지 장치다. 이 문장 외의 모든 의미 오류를 찾아내는 평가기는 아니다."),
            ("요구사항·버전·계약·내용 검사·실패·증거·미검증 범위의 예시 기록.", "기획 주장에 어떤 실행 근거가 있는지 연결한다. evidence 문자열을 실제 캡처·실행 결과 위치로 고쳐 기록한다."),
            ("로컬 HTML 양식 경로와 소속별 제출 경로 안내.", "이 셀은 파일을 제출하지 않는다. 출력된 경로의 HTML을 VS Code 파일 탐색기에서 찾고 Finder/탐색기로 표시한 뒤 브라우저로 연다. 작성본 HTML 저장 후 다시 열어 내용을 확인한다. LMS는 Learning Management System, 학습관리시스템이다."),
        ],
        "try": ["자신의 프로젝트에 맞는 내용 검증 조건1개와 실패 예시2개를 만든다.", "HTTP 성공만 보는 판단과 내용 기준을 함께 보는 판단의 차이를 적는다.", "기획서의 ‘검증 완료’ 항목을 실제 실행·시안·목표·미측정으로 나눠 수정한다."],
        "record": "어떤 근거로 버전을 채택·보류했고, 기획서의 어떤 주장이나 범위를 바꿨는가?",
    },
}

DOCKER_WALKTHROUGH = """
## 선택 확장 · 브라우저와 Prometheus에서 같은 지표 확인

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

**터미널 B · 저장소 루트**에서 기존 가상환경을 활성화한 뒤 실행한다. Mac/Linux는 `source .venv/bin/activate`, Windows는 `.venv\\Scripts\\Activate.ps1`이다.

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
"""
