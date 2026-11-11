# Ollama × Langfuse: 요청 추적에서 배포 전 검증까지

**실습 미션:** “금요일 오후, 새 상담 AI를 배포해도 될까?” 실제 반품·교환 답변을 생성하고 재고 오답을 추적합니다. 같은 질문으로 세 버전을 비교하고, 배포 조건을 충족하지 못한 변경을 차단합니다.

- [09 요청 추적 Notebook](../notebooks/09_langfuse_ollama_tracing.ipynb): 20분 핵심 실습
- [10 실험 비교·배포 조건 Notebook](../notebooks/10_langfuse_experiments_release_gate.ipynb): 25분 핵심 실습
- [강의안](https://smilesjcha.github.io/llmops-16week/week11/lecture/) · [전체 Notebook 안내](../WALKTHROUGH.md)

- [11주차 화면별 시연 순서·사전 점검](https://smilesjcha.github.io/llmops-16week/week11/lab/demo/): 준비 → 요청 트리 → 입출력 → 점수 → A/B/C 실험 → 배포 판단.

## 수업 전 준비: 설치 대기는 수업 시간 밖으로

Python **3.11**, VS Code Python·Jupyter 확장, Docker Desktop(실행 중), Ollama 앱(실행 중)이 필요합니다. 저장소 전체 폴더를 열고 `.venv`를 사용합니다. Windows는 `py -3.11 -m venv .venv` 후 `.venv\Scripts\Activate.ps1`, macOS/Linux는 다음과 같습니다.

```sh
# 저장소 루트. 기존 .venv가 있으면 생성 명령은 생략
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/week11-langfuse.txt
python -m pip check
python week11/lab/langfuse/init_env.py
ollama pull qwen2.5:1.5b-instruct
docker compose -f week11/lab/langfuse/compose.yaml up -d --wait --wait-timeout 300
docker compose -f week11/lab/langfuse/compose.yaml ps
```

처음에는 Docker 이미지·모델을 내려받으므로 **수업 전 15–30분의 준비 시간**을 확보합니다. 네트워크에 따라 더 걸릴 수 있습니다. Linux 등에서 Ollama 앱을 사용하지 않으면 별도 터미널에 `ollama serve`를 실행합니다. 이미 실행 중이면 다시 띄우지 않습니다.

실제 검증: macOS arm64, Python 3.11.14, Docker Desktop, Docker VM RAM 약 16GB. [공식 Compose 안내](https://langfuse.com/self-hosting/deployment/docker-compose)는 VM에 4코어·16GiB를 권장합니다. 이 실습도 여섯 컨테이너와 Ollama를 함께 사용하므로 수업 전에 본인 기기에서 확인합니다. 메모리가 부족한 기기의 실행 성공을 보장하지 않습니다.

### 로그인과 준비 완료 조건

1. [로컬 Langfuse](http://localhost:3011)를 엽니다.
2. VS Code에서 `week11/lab/langfuse/.env` 파일을 엽니다.
3. `LANGFUSE_LOGIN_EMAIL`과 `LANGFUSE_LOGIN_PASSWORD`로 **Sign in**합니다. 회원가입이나 이메일 인증은 필요 없습니다.
4. `LLMOps Course / Week 11 Ollama` 프로젝트를 확인합니다.
5. VS Code Notebook의 **Select Kernel → Python Environments → 저장소 .venv** 선택.
6. 09번 첫 환경 셀이 인증·모델 버전을 출력하면 준비 완료입니다.

`init_env.py`가 PC마다 무작위 비밀번호·API 키를 만들고, 공식 headless initialization으로 사용자·조직·프로젝트를 준비합니다. 다시 실행해도 기존 `.env`를 덮어쓰지 않습니다. 설정 파일은 Git 제외입니다. 다른 프로젝트의 쉘 환경 키를 가져오지 않으며, Python 연결은 로컬 주소만 허용합니다.

## 실행 구조

```text
내 PC의 VS Code / Python
  ├─ 검색·코드 검사
  ├─ 실제 생성·모델 평가 → Ollama :11434 (호스트)
  └─ 관찰 기록·점수 → Langfuse :3011 (Docker)
                        ├─ web: UI·API·인증
                        ├─ worker: 비동기 기록 처리
                        ├─ PostgreSQL: 프로젝트·설정
                        ├─ ClickHouse: 관찰·평가 데이터
                        ├─ Redis: 작업 큐
                        └─ MinIO: 이벤트 객체 저장
```

Docker는 **Langfuse 저장·표시 환경**입니다. Ollama는 호스트에서 GPU를 사용합니다. Langfuse 컨테이너가 Ollama를 대신 호출하지 않으므로 `host.docker.internal` 설정이 필요 없습니다. 평가 함수도 Notebook에서 실행한 뒤 Scores로 보냅니다. AI Gateway·클라우드 계정·UI 자동 평가기는 이 실습에 필요 없습니다.

호스트에 공개하는 포트는 `127.0.0.1:3011` 하나입니다. DB·Redis·MinIO 포트는 Docker 내부에서만 사용합니다. 이 구성은 로컬 수업용이며 외부 서버 배포용 구성이 아닙니다.

## 100분 수업 운영

| 시간 | 활동 | 완료 확인 |
|---|---|---|
| 0–10분 | 배포 상황·성공 조건·결과 예측 | “재고가 없다”와 “확인할 수 없다” 구분 |
| 10–25분 | 평가 데이터·검색 지표 핵심 / 01–04 발췌 | 검색 성공과 답변 성공의 차이 |
| 25–40분 | 실제 생성·평가 / 07–08 핵심 셀 | 답변·인용·기권·judge의 불일치 |
| 40–60분 | **09번 2–5단계** | 실제 요청 트리·입출력·Scores 확인 |
| 60–85분 | **10번 1–7단계** | A/B/C 실험과 배포 조건 비교 |
| 85–100분 | 사람 검토·개선안·판단 기록 | 보류/검토 결론 + 실패 근거 1건 |

01–08의 모든 셀을 다시 실행하지 않습니다. 계산 심화와 09번 SDK 최소 구문·사람 점수 입력·보고서 저장은 복습 가능합니다. 설치 문제가 수업 중 발생하면 이미 검증한 교수 화면과 강의안 캡처로 같은 판단 활동에 참여하고, 로컬 실행은 문제 해결 후 이어갑니다. 캡처를 실시간 실행으로 소개하지 않습니다.

### 재미와 판단이 있는 세 번의 비교

1. **먼저 예측:** 답변을 보기 전, 어느 버전이 재고 질문에 기권할지 선택합니다.
2. **근거 찾기:** Langfuse에서 실제 입력 문서와 출력, 잘못된 judge 이유를 찾습니다.
3. **배포 결정:** 평균 점수만 보지 않고, 허용할 수 없는 실패를 정해 A/B/C 중 다음 검토 대상을 고릅니다.

## 09번: 요청 한 건의 실제 기록

실행 순서: 준비 → 최소 SDK 예제 → 전체 요청 → 저장 재조회 → 점수 → 두 프롬프트 → 사람 검토 → 기록.

| 확인 위치 | 볼 내용 |
|---|---|
| Tracing / 요청 링크 | 전체 요청과 부모·자식 작업 |
| `01-retrieval` Output | 실제 검색 문서 3개·점수 |
| `02-ollama-answer` Input/Output | 모델에 전달한 메시지와 실제 답변·인용·기권 |
| `03-code-checks` | 인용·기권 계약 검사 |
| `04-ollama-judge` | 실제 모델 판정과 이유·토큰 |
| Trace의 Scores | BOOLEAN 코드 점수 / CATEGORICAL 모델 판정 |

전체 요청은 기본적으로 **부모 1개 + 하위 작업 4개**입니다. `flush()`는 전송 큐를 비우며, `wait_for_trace()`가 서버 저장을 재조회합니다. 개인 기기에서 생성되는 URL·trace ID·답변·지연은 예시와 달라집니다.

## 10번: 실험·회귀 평가·배포 판단

| 버전 | 바꾸는 것 | 학습 포인트 |
|---|---|---|
| A baseline | 기존 프롬프트 | 현재 동작을 먼저 측정 |
| B grounded | 근거 제한 프롬프트 | 지시 강화의 효과와 한계 |
| C capability_guard | B + 미지원 기능의 정책 처리 | 프롬프트와 서비스 설계의 역할 구분 |

3개 정상 사례와 재고 경계 사례 1개를 같은 데이터로 실행합니다. Datasets에는 참고 기준과 실패 trace의 연결이, Experiments에는 버전별 출력·점수·trace가 저장됩니다. **내용이 바뀐 원격 데이터는 자동 덮어쓰지 않습니다.**

C의 `requested_capability`는 상담 UI에서 선택한 **정책 안내 / 실시간 재고 조회** 메뉴 또는 API 라우트의 입력입니다. 서비스 분기는 `answerable`·정답 문서·참고 답변을 읽지 않습니다. 자유 문장의 의도 분류기는 구현하지 않았으므로 이 정책이 모든 자유형 재고 질문을 찾아낸다고 해석하지 않습니다.

미지원 실시간 조회는 실제 서비스 코드가 기권 응답을 반환합니다. 이 경로는 **LLM 호출 없음, judge 미실행**으로 표시하고, 정상 상담 3개는 실제 Ollama를 호출합니다. 모의 모델 출력으로 채우는 방식이 아닙니다.

배포 전 조건은 실험 전에 고정합니다.

- 답변 불가 질문의 수락 0건
- 인용·기권 계약 검사 100% 통과
- 기준선보다 계약 검사 통과율이 떨어지지 않음
- 생성 요청별 3초 이내: 교육용 기본 예산, 기기·서비스 요구에 따라 실험 **전에** 조정
- 모든 문항 실행 완료: 누락·실패를 평균에서 빼지 않음

**HOLD**는 보류, **REVIEW**는 사람 검토 대상입니다. 4건의 계약 검사 통과율을 의미 정확도로 소개하지 않습니다. 작은 모델의 자기 평가는 독립 검증이 아니며, 4건으로 p95 지연이나 일반 성능을 추정하지 않습니다. 실제 운영 배포·롤백 명령은 실행하지 않습니다.

### 터미널로 미리 검증

```sh
python -m week11.lab.langfuse_lab
python -m week11.lab.release_lab
# B 프롬프트 후보가 HOLD이면 종료 코드 2: 의도된 배포 전 차단
python -m week11.lab.release_lab --enforce-gate
```

결과는 `week11/lab/reports/langfuse/`에 저장합니다. CLI와 Notebook을 재실행하면 새로운 실험 기록이 추가됩니다. 강의 화면의 값에 맞추려고 원응답을 수정하지 않습니다.

## 중지·재개와 문제 해결

```sh
# 종료: 데이터 보존
 docker compose -f week11/lab/langfuse/compose.yaml stop
# 재개
 docker compose -f week11/lab/langfuse/compose.yaml up -d --wait --wait-timeout 300
# 상태와 필요한 서비스의 최근 로그
 docker compose -f week11/lab/langfuse/compose.yaml ps
 docker compose -f week11/lab/langfuse/compose.yaml logs --tail 60 langfuse-worker
```

| 증상 | 확인·조치 |
|---|---|
| Docker daemon 연결 실패 | Docker Desktop 실행 후 재시도 |
| 이미지 다운로드·시작 지연 | 수업 전에 pull 완료. Docker 메모리·디스크 확인 |
| 3011 포트 충돌 | 해당 포트를 사용하는 프로그램 확인. `.env`의 PORT와 BASE_URL을 함께 변경 후 `up -d` |
| 인증 실패 | `.env`를 재생성하지 않았는지, 최초 초기화한 DB와 같은 키인지 확인 |
| 화면에 trace가 없음 | 같은 프로젝트·환경·시간 범위인지 확인, `flush()` 후 재조회, worker 상태 확인 |
| Scores만 늦게 보임 | 비동기 처리 대기 후 새로고침. timeout을 성공으로 숨기지 않음 |
| Ollama 모델 없음 | `ollama list`, `ollama pull qwen2.5:1.5b-instruct` |
| 답변은 확인 불가인데 기권 false | 실행 오류가 아닌 모델의 계약 위반. B/C 비교 실습에서 분석 |
| Notebook import 실패 | `.venv` 커널과 week11-langfuse requirements 설치 확인 |

일반 종료에는 `down -v`를 사용하지 않습니다. DB volume과 `.env`는 한 쌍으로 보관합니다. SDK 5.2.0은 Langfuse v4 계열용이며, 과거 주차의 Langfuse 3.x 설치 프로필과 섞지 않습니다.

## 공식 근거와 고정 버전

- 서버 web/worker: **4.78.0**, Python SDK: **5.2.0**, 세부 SDK 의존성은 [고정 목록](../../../requirements/locks/week11-langfuse-sdk-py311.txt).
- [공식 Compose](https://github.com/langfuse/langfuse/blob/v4.78.0/docker-compose.yml)를 로컬 수업 범위로 축소했습니다.
- [Headless initialization](https://langfuse.com/self-hosting/administration/headless-initialization)
- [SDK instrumentation](https://langfuse.com/docs/observability/sdk/instrumentation)
- [Scores via SDK](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)
- [Experiments via SDK](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)

확인일: 2026-11-11. 키·비밀번호·로그인 세션은 공개 저장소에 포함하지 않습니다. 강의 캡처는 이 로컬 합성 사례의 실제 화면입니다.
