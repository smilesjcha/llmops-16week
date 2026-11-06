# 10주차 · 80쪽과 100분 수업 진행안

## 목적과 자료의 역할

주제는 **LLM 서비스 배포와 실행 관찰**이다. 9주차 API 계약을 반복하기보다 실행 버전·계측·원인 탐색·복구·배포 판단을 연결한다. 80쪽은 강의와 복습 자료를 함께 담는다. 모든 장표를 같은 속도로 읽거나 전체 Notebook을 수업 중 완주하지 않는다.

[장표별 도구·서비스 기능 해설](TOOL_EXPLANATIONS.md)에 OpenTelemetry·SDK·Collector·Prometheus·Docker·앱 서버의 설명 문장, 시연 화면, 학생 질문과 현재 구현 범위를 정리했다. Notebook6개에는 실행 위치·예상 결과·해석·복습 실험·오류 해결표를 넣었다. Notebook04는 Docker/Prometheus, Notebook05는 브라우저 장애·복구의 선택 확장을 포함한다.

| 시간 | 핵심 장표 | 진행 |
|---|---|---|
| 00–08분 | 1–8 | 200 응답의 잘못된 답변 사례·실제 화면·로드맵 |
| 08–20분 | 10–13·16·18·21–25 | 릴리스·환경·포트·준비 상태 |
| 20–30분 | 27–30·32–34·37–42 | 공식 도식·로그 연결·Span·실패 지점 |
| 30–40분 | 46–58·60–67 중 선택 | 분모·버킷·복구·릴리스 회귀 |
| 40–45분 | 70–71 | 휴식·커널·서버 점검 |
| 45–52분 | Notebook01·02 핵심 | manifest·lifespan·로그 조회 |
| 52–60분 | Notebook03·브라우저 | 정상 Trace·context·검색 오류 |
| 60–68분 | Notebook04 핵심 | 2/5 분모·버킷·reset |
| 68–76분 | Notebook05 핵심 | ready 실패·504·정상 복구·active0 |
| 76–85분 | Notebook06 핵심 | v1/v2 비교·200과 내용 기준의 분리 |
| 85–100분 | 72–80 | 기획서 개선·증거 리뷰·제출 공지 |

48–51쪽 Docker/Prometheus는 교수가 수업 전에 실행해둔 화면으로 약4분 시연하거나 선택 복습으로 둔다. 학생은 공통 Notebook에 집중하고 이미지 다운로드·Docker 설치는 수업 전에 준비한다. Notebook은 각각 독립 실행 가능하고 전체 권장 분량은 약84분이다.

## 도입 사례와 관찰의 질문

2쪽의 v2는 200이지만 잘못된 고정 답변을 반환한다. “이 버전을 배포할 수 있는가”를 학생에게 먼저 묻고, 서비스가 살아 있다는 증거와 내용이 요구사항을 만족한다는 증거를 구분한다. 실제 모델 정확도 시험이 아니라 명백한 회귀를 재현한 fixture임을 설명한다.

10–20쪽은 코드·모델·프롬프트·데이터·명세·실행 설정을 따로 기록한다. config_id는 허용 설정 JSON의 지문이고 Git commit이나 이미지 digest를 대신하지 않는다. 12–17쪽은 venv와 컨테이너의 경계를 비교한다. 17쪽은 운영체제별 Docker 설치와 엔진 준비 확인이다. 선택 Compose의 API 이미지 빌드·컨테이너 기동·Prometheus 수집은 Mac Colima/Linux arm64에서 실제 확인했다. Windows·Intel Mac 설치는 학생 기기별 공식 안내를 따른다.

## 상태 검사

21–24쪽은 Kubernetes의 검사 개념을 참고하지만 클러스터를 설치하지 않는다. 실습의 startup은 lifespan 상태이고, readiness는 started·draining·의존성 fixture의 조합이다. 검사 endpoint가 있다고 로드밸런서 정책이 저절로 구현되는 것은 아니다. 외부 의존성만 장애인 경우 프로세스 재시작을 반복하는 선택이 적절한지 질문한다.

## 로그와 Trace

28·30쪽은 OpenTelemetry 공식 원본 도식이다. 저자·라이선스·회색조 표시를 명시했다. 공식 도식의 분산 서비스 구조와 이번 한 프로세스의 직접 구현 계측을 혼동하지 않도록 설명한다. 공식 SDK·Exporter·Collector·Trace 백엔드는 확장 주제다. 지표만 선택 Compose에서 Prometheus로 수집한다.

32–36쪽은 완료 로그의 허용 필드를 살핀다. message·answer·IP·예외 원문을 넣지 않는다. 보존 제한200건과 누적 counter는 범위가 다르다. request_id로 로그를 찾고 trace_id로 작업을 모은다. ID는 인증 증거가 아니다.

37–44쪽은 parent_id와 기간의 포함 관계를 확인한다. 입력 검증422는 endpoint 진입 전이라 로그만 있고 assist Span은 없다. 검색 오류는 generate를 실행하지 않는다. generate ERROR만으로 외부 GPU 작업이 취소됐다고 말하지 않는다. 교육용 traceparent 파서는 전체 W3C 구현이 아니며 샘플링 정책도 제공하지 않는다.

## 집계와 장애

46–58쪽은 전체 assist 요청에서5xx를 나누는 분모 정의다. 이번 분모에422는 포함되고 UI·프로브·스크레이프는 제외된다. histogram 버킷은 이하 누적 개수여서 단순 합산할 수 없다. 요청0을 성공100%로 읽지 않고, counter reset이 있으면 구간 차이 계산을 중단한다. 실제 SLO·장기 알림 임계값은 확정하지 않는다.

60–69쪽은 증상→근거→완화→재검증을 연결한다. Notebook05의 dependency_ok 변경은 로컬 테스트 fixture이며 운영 관리 API가 아니다. Notebook06의 v1 복원은 새 앱을 만들어 확인하는 로컬 비교다. 실제 Canary·Blue-Green·트래픽 전환을 완료한 것으로 소개하지 않는다. 200과 내용 기준을 동시에 보는 배포 gate의 이유가 핵심이다.

## 선택 시연 · 실제 Prometheus

수업 전 [QUICKSTART](../QUICKSTART.md)의 Docker 준비·Compose 시작을 마친다. 첫 이미지 다운로드를 수업 중 기다리지 않도록 한다. 기존8010포트 Python 서버를 먼저 종료한다. 공통 Notebook은 별도 앱을 생성하므로 Compose 실행과 독립이다.

1. 48쪽: 앱이 현재 숫자를 노출하고 Prometheus가5초마다 수집·저장하는 방향 설명.
2. 49–50쪽: 두 컨테이너와 `/targets`의 UP 확인. UP은 지표 수집 가능의 증거다.
3. 새 컨테이너에서 seed30건 실행. 51쪽과 같은200=18·502=6·504=6은 새 실행의 예상 건수다. 기존 요청이 있으면 누적값은 다르다.
4. `/query`에서 `lab_assist_requests_total{job="week10-api"}` 실행 후 Table·Graph 전환. 원래 화면의5분 범위와 수집 시각을 함께 읽는다.
5. 시간 여유 시 queries.promql의rate와 오류 비율 확인. 요청이 없는 창의NaN·빈 결과를 성공100%로 읽지 않는다. 짧은 active 작업은5초 간격에서 놓칠 수 있다.

공통 Notebook04의 snapshot 차이와 Prometheus의시간창rate는 측정 방식이 다르다. 이 시연은 고정 응답 서비스이며 실제 LLM 처리량 시험·분산Trace·Grafana·운영 알림은 포함하지 않는다. 종료는 자신이 띄운 Compose 프로젝트의down만 사용한다.

## 기획서 리뷰와 공지

72–75쪽은 사용자 문제·변경·시험·판단 근거를 연결한다. 단일 또는 복수 포트폴리오를 허용하고 결과물 수·도구 수를 자동 평가 점수로 쓰지 않는다. 실제 실행·고정 시안·목표·미측정을 나누어 기록한다.

**마지막 78–80쪽 공지:** 기획서2차는 **2026년11월6일(금) 오늘 제출**, 미제출자는 **늦어도11월7일(토)까지 제출 요청**이다. 확정되지 않은 마감 시각·감점 정책은 추가하지 않는다. 아주대AI대학원은LMS, 군산대·창원대 등 별도 수강생은 공지된 담당 교수 이메일을 이용한다. PPT·Word 기반PDF·HTML 등에서 선택하며 HWP/HWPX는 제외한다.

## 검증·재생성

```bash
python scripts/build_week10_notebooks.py
python scripts/verify_week10_notebooks.py
python scripts/verify_week10_live.py
```

차트 입력은 `lecture/assets/measurements.json`에 공개한 합성 실험의 필요한 집계다. 재측정 시 원시 receipt를 검토하고 날짜·단위·조건과 함께 입력을 갱신한 뒤 PPT·PDF를 재생성한다. 슬라이드 생성은 공통 빌드 환경에서 `scripts/build_course_deck.mjs 10`을 사용한다. 브라우저 캡처 스크립트는 Playwright와 실행 가능한 브라우저가 필요하며 `CHROMIUM_EXECUTABLE`로 설치된 실행파일을 지정할 수 있다. 학생 필수 도구가 아니다.
