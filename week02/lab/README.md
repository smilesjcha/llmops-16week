# PROMPT/02 · 고객 문의 분류와 프롬프트 비교

한 번 좋아 보이는 답변보다 **동일한 입력에서 무엇이 달라졌는지 설명할 수 있는 변경**을 만드는 2주차 실습입니다. 작년 4개 노트북의 문제 정의, 출력 형식, 소수 예시, 업무 분기, 오류 처리를 하나의 고객지원 업무로 연결했습니다. 원본은 `AS-IS 2025 2nd semester/practice/week02/`에 그대로 보존합니다.

필수 실습은 API 키·모델 다운로드·유료 호출 없이 끝납니다. 선택 실습만 로컬 Ollama를 사용합니다. 실제 고객 정보, 실제 주문 처리, 환불 실행, 외부 메시지 발송은 없습니다.

## 시작

저장소 루트에서 기존 공통 `.venv`를 사용합니다. 기준은 CPython 3.11.14이며 추가 패키지는 없습니다. 설치가 필요하면 [VS Code 가이드](../VS_CODE_GUIDE.md)를 따라갑니다.

```bash
.venv/bin/python -m uvicorn prompt02.main:app --app-dir week02/lab --port 8002
```

[실습 화면](http://127.0.0.1:8002), [API 대화형 문서](http://127.0.0.1:8002/docs), [상태 확인](http://127.0.0.1:8002/health).

서버는 이 터미널에서 계속 실행됩니다. 추가 명령은 다른 터미널에서 실행하고, 종료는 서버 터미널에서 `Ctrl+C`입니다. 1주차 서버 8000번과 충돌하지 않습니다.

## 45분 필수 실습

| 시간 | 화면 / 작업 | 확인할 내용 |
|---|---|---|
| 0–7분 | STEP 01 · demo 실행 | 합성 문의 8건, 동일한 입력, 실제 모델이 아닌 고정 응답 |
| 7–17분 | STEP 02 · v1/v2/v3 미리보기 | v2의 출력 형식과 업무 규칙, v3의 별도 예시 3건 |
| 17–30분 | STEP 03 · 결과 상세 | T01 형식 실패, T03 분류 오류, T08 미확정 환불 약속 |
| 30–38분 | STEP 04 · 선택 근거와 JSON 저장 | 개선 근거, 남은 한계, 다음 평가 사례 |
| 38–45분 | 오류 해석 / 선택 Ollama / 종료 | 호출 실패와 모델 출력 실패 구분, 자동 전환 없음 |

1. `demo · 오프라인 시뮬레이션`과 8건 선택을 확인합니다.
2. `3개 버전 비교 실행`을 누릅니다. 같은 문의에 대한 24개 결과를 확인합니다.
3. T01의 v1 결과를 열면 문장은 자연스럽지만 JSON 형식은 실패합니다.
4. T03의 v2 결과는 형식이 맞아도 교환 문의를 환불로 분류합니다. 기대 결과와 판단 근거를 읽습니다.
5. T08의 v2 결과는 당일 환불을 확정합니다. 주문·승인 정보가 없는데 결과를 약속했는지 확인합니다.
6. v3의 예시가 다루는 경계 기준을 읽고 후보 선택 근거를 15자 이상 작성합니다.
7. `결정 기록 추가` 후 `JSON 보고서 내보내기`를 눌러 보관합니다.

예시 기록: “v3에서 복합 문의의 첫 번째 요청과 담당자 검토 기준을 확인했다. 현재 결과는 고정 응답 8건이므로 실제 모델과 별도 문의 세트에서 재평가한다.”

## 결과를 읽는 기준

| 검사 | 코드 필드 | 의미 |
|---|---|---|
| 형식 | `format_ok` | JSON 구문, 중복 키 금지, 필수 필드, 자료형, 허용값, 추가 필드 금지 |
| 분류 | `routing_ok` | `category`가 이 데이터 세트의 기대 분류와 같은지 |
| 확정 약속 | `promise_ok` | 제한된 정규표현식으로 미확정 환불·입금·배송 확약을 탐지하지 않았는지 |
| 검토·우선순위 | `review_ok` | `needs_review`와 `priority`가 기대 기준과 같은지 |
| 전체 통과 | `overall_ok` | 위 네 검사를 모두 통과했는지 |

형식 실패 시 의미 검사는 `null`(미평가)입니다. 모델 호출 자체가 실패한 경우 형식 검사도 미평가입니다. 화면 성공률의 분모는 **전체 선택 문의 수**이며, 내보낸 JSON의 `evaluated`는 실제 평가된 건수를 따로 제공합니다. 지연시간 평균은 오류·미실행을 제외한 응답 건수만 사용하고 `latency_sample_count`를 함께 기록합니다. 지연 샘플 0건의 표시값 0ms는 성능 측정값이 아닙니다.

정답 기준은 실습의 업무 규칙입니다. 실제 회사 정책이나 보편적 정답이 아닙니다. `data/cases.json`의 `rationale`에 각 판단 근거가 있습니다. 예를 들어 T07은 교환을 먼저 요청하므로 exchange로 분류하고, 대안인 환불 요청도 있어 담당자 검토를 표시합니다.

### 반드시 구분할 점

- **demo는 고정 응답을 재생하는 교육용 시뮬레이션**입니다. v1 0/8, v2 4/8, v3 8/8 전체 통과 결과는 정해진 예시이며 실제 LLM 성능이나 예시 추가의 일반적 개선 효과가 아닙니다.
- `prompts/*.md`를 고쳐도 demo 응답은 바뀌지 않습니다. 바뀐 프롬프트 해시와 미리보기만 확인할 수 있습니다. 응답 변화를 측정하려면 동일 조건의 실제 모델 실행이 필요합니다.
- 이 8건은 공개된 개발용 평가 세트입니다. 운영 채택 근거를 만들려면 프롬프트 개선에 사용하지 않은 별도의 데이터가 필요합니다.
- `promise_ok`는 완전한 의미 판별기가 아닙니다. “오늘 환불을 보장할 수 없습니다” 같은 부정문도 오탐할 수 있고 우회 표현은 놓칠 수 있습니다. 한국어 답변 품질, 모든 사실 오류, 완전한 프롬프트 주입 방어는 자동 검증하지 않습니다.
- 문의를 JSON으로 분리하고 시스템 메시지와 구분해도 프롬프트 주입이 원천 차단되지는 않습니다. 모델 출력은 실행하지 않고 업무 실행 권한도 제공하지 않습니다.
- 후보 선택은 교육용 결정 기록입니다. 자동 배포나 실제 고객 업무는 일어나지 않습니다.

## 출력 명세

```json
{
  "category": "exchange",
  "priority": "normal",
  "needs_review": true,
  "reply": "교환 가능 재고를 먼저 확인하고 담당자가 후속 절차를 안내하겠습니다."
}
```

`category`: delivery / refund / exchange / account / other. `priority`: normal / urgent. `needs_review`: JSON 불리언. `reply`: 공백 정리 후 5–160자. 추가 필드는 허용하지 않습니다. 정확한 JSON Schema는 `/api/catalog`의 `output_schema`와 `prompt02/contracts.py`에 있습니다.

## 선택 실습 · Ollama

Ollama가 설치된 환경에서 다음 명령을 별도 터미널에 실행합니다.

```bash
ollama --version
ollama list
ollama pull qwen3:4b-instruct
ollama run qwen3:4b-instruct "한국어로 준비 완료라고만 답하세요."
```

`ollama pull`은 모델 파일을 다운로드하므로 네트워크와 디스크가 필요합니다. Ollama 앱이 실행 중이면 `ollama serve`를 중복 실행하지 않습니다. 연결이 안 되는 경우에만 새 터미널에서 `ollama serve`를 실행합니다.

화면 실행 모드를 Ollama로 바꾸면 T01 한 건만 선택됩니다. 모델 로딩을 먼저 마친 뒤 비교합니다. 기본 설정은 `qwen3:4b-instruct`, `think:false`, `temperature:0`, `seed:42`, `num_ctx:4096`, `num_predict:384`, `keep_alive:"30m"`입니다. 개별 호출은 최대 35초, 실험 전체는 최대 120초입니다. 오류가 발생하면 반복 요청을 중단하고 나머지는 미실행으로 기록합니다. demo로 자동 전환하지 않습니다.

프롬프트만 비교하기 위해 세 버전 모두 동일한 모델 옵션을 사용하며 Ollama의 `format` 옵션은 설정하지 않습니다. JSON Schema 기반 구조화 출력은 별도 실험 요인입니다. 이를 켠 결과와 프롬프트만 바꾼 결과를 같은 실험으로 해석하지 않습니다.

다른 로컬 모델을 사용할 때는 `.env.example`을 `.env`로 복사하고 모델명을 수정한 다음 명시적으로 로드합니다.

```bash
cp week02/lab/.env.example week02/lab/.env
.venv/bin/python -m uvicorn prompt02.main:app --app-dir week02/lab --port 8002 --env-file week02/lab/.env
```

기본 실행은 `.env`를 자동으로 읽지 않습니다. 주소는 로컬 호스트만 허용합니다. 모델 태그만 같아도 모델 파일·Ollama 버전·하드웨어가 다르면 결과와 시간이 달라질 수 있으므로 별도 기록합니다.

## 터미널과 노트북

```bash
# 서버 없이 전체 demo 비교
PYTHONPATH=week02/lab .venv/bin/python -m prompt02.run_experiment --provider demo

# 고유한 경로로 결과 저장 (이미 있는 파일은 덮어쓰지 않음)
PYTHONPATH=week02/lab .venv/bin/python -m prompt02.run_experiment --provider demo --output /tmp/prompt02-my-first-run.json

# 실제 모델: 우선 문의 한 건
PYTHONPATH=week02/lab .venv/bin/python -m prompt02.run_experiment --provider ollama --cases T01

# 실행 중인 서버 점검
PYTHONPATH=week02/lab .venv/bin/python -m prompt02.smoke --url http://127.0.0.1:8002

# API·검증 규칙·오류 처리 테스트
.venv/bin/python -m pytest week02/lab/tests -q
```

Windows에서는 macOS/Linux 경로로 구성된 VS Code 자동 작업을 사용하지 않습니다. [Windows PowerShell 실행 순서](../VS_CODE_GUIDE.md#6-windows-powershell-실행-순서)의 설치·서버·점검 명령을 사용합니다. `PYTHONPATH=...` 대신 `$env:PYTHONPATH="week02/lab"`를 먼저 실행하고, Python 경로는 `.\.venv\Scripts\python.exe`를 사용합니다. Windows와 Linux의 실제 실행 검증은 아직 진행하지 않았습니다.

[실행 가능한 안내 노트북](week02_prompt02_lab.ipynb)은 위 흐름을 코드로 확인합니다. 모든 필수 셀은 오프라인으로 실행되며 선택 Ollama 셀은 기본적으로 비활성화되어 있습니다.

## 구성

```text
week02/lab/
├── prompt02/                  API, 실행, 검증, 정적 UI
│   ├── contracts.py           요청 / 출력 명세
│   ├── core.py                프롬프트 렌더링, 해시, 검사, 집계
│   ├── providers.py           고정 응답 / 로컬 Ollama
│   ├── experiments.py         동일 조건 비교와 시간 상한
│   ├── main.py                API와 메모리 기록
│   ├── run_experiment.py      명령줄 비교
│   ├── smoke.py               전체 동작 확인
│   └── static/                브라우저 화면
├── prompts/v1.md, v2.md, v3.md 편집 가능한 프롬프트 원문
├── data/cases.json            합성 평가 문의와 기대 기준
├── data/demo_responses.json   설명용 고정 응답
├── tests/                     의미 있는 오프라인 검증
└── week02_prompt02_lab.ipynb   셀 단위 안내 노트북
```

보고서에는 데이터 해시, 선택 입력 세트 해시, 프롬프트 원문 스냅샷과 해시, 렌더링된 프롬프트 해시, 평가기 버전, 실행 설정, 지연시간, 원문 응답, 검사 결과, 선택 이유가 담깁니다. 최근 30개 실험과 실험당 20개 결정만 서버 메모리에 저장됩니다. 서버 재시작 전 파일로 내보내세요.

기술 명세 확인: [Ollama Chat API](https://docs.ollama.com/api/chat), [Ollama Thinking 설정](https://docs.ollama.com/capabilities/thinking), [qwen3:4b-instruct 모델](https://ollama.com/library/qwen3:4b-instruct), [Pydantic Strict Mode](https://docs.pydantic.dev/latest/concepts/strict_mode/). 확인일: 2026-09-11.
