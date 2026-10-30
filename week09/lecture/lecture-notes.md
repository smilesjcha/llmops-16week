# API 계약과 LLM 서비스 구현

## 1. API 계약과
LLM 서비스 구현

WEEK 09 · 2026.10.30 · 온라인 실시간

입출력 계약 · 실패 복구 · 비교 실험

차성재 · 무신사 Core AI PM × AI 대학원 겸임교수

기획서에 적은 사용자 흐름을 실제 요청과 응답으로 옮기는 주차다. 오늘 구현할 기능은 하나의 합성 안내 서비스이며 기술 이름을 나열하기보다 성공·실패·중단의 계약을 확인한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 2. 이번 주의 완료 증거

계약 · 정상 응답·입력 오류를 구분하는 API

복구 · 시간 초과·거절·중단 이후 자원 해제

실험 · 조건·표본·성공 지연·오류율의 기록

강의 포인트: API · Application Programming Interface · 응용 프로그래밍 인터페이스

완료 증거는 화면 한 장이 아니라 실행 명령과 재현 가능한 입력이다. 정상 한 건, 잘못된 입력 한 건, 시간 초과 한 건, 사용자 중단 한 건을 같은 버전에서 확인하면 서비스 경계를 설명하기 쉬워진다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 3. 16주 로드맵 · 9주차



기획서 수정본의 제출 마감은 10월22일이었다. 10월23일은 시험·실시간 수업 없이 평가했다. 오늘은 10월30일 온라인 실시간 수업이며 새 제출 일정을 추정하지 않는다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 4. 기획서에서 실행 계약까지

요구사항 · 사용자·실패

API 명세 · 입력·출력

검증 코드 · 성공·오류

실행 근거 · 판단·한계

강의 포인트: 8주차 문서를 다시 쓰기보다, 요구사항 하나를 실행 가능한 기능으로 연결

기획서의 기능 요구사항을 하나 고른 뒤 누가 어떤 입력을 보내고 어떤 필드를 받는지 적는다. 다음으로 잘못된 입력과 외부 장애를 구분하는 시험을 만든다. 오늘 자료가 실제 프로젝트의 모든 요구를 구현한 것은 아니다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 5. 100분 수업 구성

시간 · 학습·활동

00–20분 · 문제·API 계약·실패 응답

20–40분 · 비동기·용량·캐시·추론 구조

40–45분 · 휴식·환경·커널 확인

45–85분 · 선택 핵심 셀·브라우저·실패 복구

85–100분 · 부하 결과·프로젝트 리뷰

강의 포인트: 전체 Notebook 85분 분량 · 수업은 핵심 셀, 나머지는 복습

100분 안에 모든 세부 장표와 53개 코드 셀을 완독하지 않는다. 계약·용량·스트리밍·지표 해석의 핵심 셀을 함께 실행하고 상세 캐시 실험과 선택 제공자는 복습에서 확장한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 6. 실행 중인 반품 안내 서비스

한 명의 질문에는 정상 응답

동시 접속에서는 대기·중단·잘못된 입력이 발생

오늘의 대상은 답변 함수 주변의 서비스 동작

강의 포인트: 합성 정책·고정 응답으로 운영 구조를 실험 · 실제 고객 정책 아님

한 명에게 답변하는 함수가 잘 동작해도 수십 명이 동시에 요청하거나 브라우저를 닫으면 다른 문제가 생긴다. 실제 고객 정책을 검증하는 수업이 아니므로 응답 문구 앞에 합성 정책 또는 MOCK 표시를 유지한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 7. 노트북 함수와 서비스 API

노트북 함수 · 개발자가 입력·예외를 직접 확인 · 커널 안의 한 실행 흐름

서비스 API · 서로 다른 클라이언트의 동시 요청 · 명시적 계약·실패 응답·자원 한도

함수에서는 예외를 개발자가 직접 읽지만 서비스에서는 사용자 화면과 클라이언트 코드가 다음 행동을 알아야 한다. 출력 형태와 실패 코드를 고정하면 다른 팀원이 UI와 테스트를 독립적으로 만들 수 있다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 8. 클라이언트·API·모델의 경계



강의 포인트: 이번 실습은 한 프로세스 · 외부 모델은 선택 · 인증·영구 저장은 미구현

브라우저는 API에 요청하고 API가 입력을 검증한 뒤 제공자를 호출한다. Python 함수·웹 서버·모델 서버는 서로 다른 역할이며 Uvicorn worker를 늘려도 모델 GPU가 자동으로 늘지 않는다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 9. 한 요청의 왕복 경로



강의 포인트: 검증 실패는 모델 호출 전 종료 · 요청 ID로 결과와 메타데이터 연결

클라이언트 요청을 받자마자 모델을 호출하지 않는다. 입력 검증·유입 제한·처리 용량·캐시를 통과한 후에 제공자를 호출한다. 입력 오류는 모델 비용 없이 종료하고 요청 ID는 사용자 응답과 내부 메타데이터를 연결한다.

근거: https://fastapi.tiangolo.com/tutorial/response-model/, https://www.rfc-editor.org/rfc/rfc9110.html, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 10. 오늘의 실습 화면

요청 조건 · 메시지·캐시·장애 주입

응답 계약 · 상태·요청 ID·버전

실행 경계 · MOCK 고정 응답 표시

강의 포인트: 실제 로컬 실행 화면 · 세부 JSON은 다음 장표에서 확대

화면은 저장소의 실제 index.html을 로컬 서버에서 실행한 캡처다. 같은 질문을 두 번 실행하고 cached와 provider_calls를 확인한다. 숫자는 기기와 실행 시점의 관측값이며 서비스 목표나 모델 속도 기준이 아니다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 11. 요청·응답 계약

정상 입력만 정의하는 명세의 한계

입력 검증·상태 코드·버전·완료 조건

API 명세는 정상 응답의 필드만으로 완성되지 않는다. 최대 입력, 허용 타입, 오류 상태, 버전 호환성, 스트림 완료의 의미도 계약이다. 이 계약을 테스트로 바꾸면 구현 변경의 영향을 빠르게 확인할 수 있다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 12. HTTP 요청의 구성

POST /api/v1/chat
Content-Type: application/json

{"message": "반품 정책",
 "max_tokens": 64,
 "use_cache": true}

전송 계약의 분리

경로·메서드·헤더·본문

JSON 문법과 업무 의미는 별도

강의 포인트: HTTP · Hypertext Transfer Protocol · JSON · JavaScript Object Notation

POST 경로, Content-Type 헤더, JSON 본문은 서로 다른 정보다. 문법상 올바른 JSON도 message가 공백이면 업무 입력으로 유효하지 않다. HTTP 전송 성공과 생성 결과의 의미 정확성도 구분한다.

근거: https://www.rfc-editor.org/rfc/rfc9110.html, https://fastapi.tiangolo.com/tutorial/response-model/

## 13. Pydantic 입력 모델

class ChatRequest(BaseModel):

    model_config = ConfigDict(extra="forbid", strict=True)

    message: str = Field(min_length=1, max_length=1000)

    max_tokens: int = Field(default=64, ge=8, le=128)

강의 포인트: 공백 검사 추가 · 숫자 문자열·임의 필드 거부 · app.py의 실제 계약과 연결

extra=forbid는 알 수 없는 필드를 거부하고 strict=True는 숫자 문자열의 암묵적 변환을 줄인다. message의 공백 제거·빈 값 검사는 별도 validator에서 수행한다. 수업은 공통 requirements에 고정한 Pydantic 2.11.7을 사용한다.

근거: https://fastapi.tiangolo.com/tutorial/response-model/, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 14. 필드의 의미와 한도

필드 · 계약 · 확인

message · 1–1000자·공백 제거 · 공백만 있으면 422

max_tokens · 정수 8–128 · MOCK 토큰 수 보장 아님

use_cache · 불리언 · 일반 응답만 적용

scenario · MOCK 장애 주입 · 실제 제공자는 normal만

강의 포인트: 문자 수·토큰 수·바이트 크기는 서로 다름

max_tokens는 실제 제공자에 넘기는 생성 상한이다. MOCK은 고정 문장을 반환하므로 그 문자의 길이를 토큰 수라고 표시하지 않는다. 전체 요청 바이트 크기 제한은 현재 실습 외의 배포 전 보완 사항이다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 15. 422 오류의 안전한 응답

{"error": {
  "code": "validation_error",
  "fields": [{
    "location": ["body", "message"],
    "type": "string_too_short"
  }]
}, "request_id": "..."}

수정 가능한 입력 오류

원문 입력은 오류에 복사하지 않음

클라이언트는 입력 수정 안내

강의 포인트: 422 · 입력 검증 실패 · 무조건 재시도로 해결하지 않음

프레임워크의 기본 검증 오류에는 입력값이 포함될 수 있어 교육용 앱은 위치와 오류 유형만 반환한다. 메시지나 비밀정보가 예외 응답·접근 로그·모니터링에 복제되는 경로를 점검한다.

근거: https://fastapi.tiangolo.com/tutorial/response-model/, https://fastapi.tiangolo.com/tutorial/handling-errors/, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 16. 정상 응답의 버전 정보

{"request_id": "...",
 "output": "[MOCK] ...",
 "provider": "mock",
 "model": "teaching-mock-v1",
 "prompt_version": "v1",
 "cached": false,
 "simulated": true}

다시 확인 가능한 결과

상태 200과 의미 정확성은 별개

버전·캐시·모사 여부를 함께 표시

강의 포인트: response_model=ChatResponse · 응답에 허용할 필드 명시

응답 모델은 서비스가 반환할 필드를 제한하고 문서화한다. 요청 ID는 호출마다 새로 발급하지만 캐시된 답변은 재사용될 수 있다. 200과 simulated=true는 전송 및 모사 여부이지 실제 업무 정확도 점수가 아니다.

근거: https://fastapi.tiangolo.com/tutorial/response-model/, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 17. 프로세스 상태와 준비 상태

GET /health · 프로세스가 응답하는지 확인 · 모델의 존재·생성 성공 보장 없음

GET /ready · MOCK 준비 또는 Ollama 설치 확인 · 실제 생성 성공은 별도 점검

health가 성공해도 모델 서버가 꺼져 있을 수 있다. ready의 Ollama 경로는 설치 목록에서 정확한 모델 태그만 검사하며 모델을 다운로드하거나 생성하지 않는다. 실제 짧은 생성과 품질 평가는 별도 확인한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 18. OpenAPI와 클라이언트 검사

명세 생성 · /openapi.json

수동 확인 · /docs

반복 검사 · HTTPX

변경 검토 · 호환성

강의 포인트: OpenAPI · API 명세 형식 · 문서 화면과 자동 테스트를 함께 활용

OpenAPI는 요청·응답 구조의 공유 언어다. /docs에서 한 번 실행한 성공 사례를 반복 검증으로 대체할 수 없으므로 HTTPX 테스트도 유지한다. 자동 문서가 모델 품질·권한 정책까지 검증해 주지는 않는다.

근거: https://fastapi.tiangolo.com/tutorial/response-model/, https://www.python-httpx.org/advanced/transports/

## 19. 경로 버전과 동작 버전

/api/v1 · 클라이언트 입출력 계약의 버전 · 삭제·타입 변경은 호환성 검토

prompt_version · model · 같은 API 내부의 생성 동작 · 캐시·평가·비교 조건에 반영

API 경로 버전은 클라이언트 호환성과 연결되고 프롬프트·모델 버전은 같은 계약 안의 결과 변화와 연결된다. 모델 변경 후 같은 캐시를 재사용하면 이전 결과가 남을 수 있으므로 생성 의미를 바꾸는 설정을 키와 실행 기록에 반영한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 20. 서버 없이 가능한 계약 검사

app = create_app()

transport = httpx.ASGITransport(app=app)

async with httpx.AsyncClient(

    transport=transport, base_url="http://lab") as client:

    r = await client.post("/api/v1/chat",

                          json={"message": "반품 정책"})

assert r.status_code == 200

강의 포인트: Notebook 01 · 실제 네트워크·Uvicorn 성능 측정과 구분

ASGITransport는 HTTPX 요청을 메모리 안의 앱에 직접 전달한다. 서버 포트가 필요 없고 입력 검사가 빨라지지만 DNS·TCP·프록시·실제 스트림 도착 간격은 검증하지 않는다. 앱에 lifespan 자원이 생기면 수명주기 실행도 별도 관리해야 한다.

근거: https://www.python-httpx.org/advanced/transports/, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 21. 오류 코드와 다음 행동

상태 · 실습 의미 · 다음 행동

422 · 입력 계약 위반 · 필드·길이·타입 수정

429 · 요청 빈도 제한 · 빈도·재시도 예산 조정

502 · 상류 응답 오류 · 모델명·상류 응답 확인

503 · 용량 초과·연결 불가 · 용량·포트·제공자 확인

504 · 제한시간 초과 · 시간 예산·상류 생존 확인

강의 포인트: 같은 상태의 원인은 error.code로 구분 · Retry-After는 보장 시간이 아님

코드별 복구 안내를 읽고 어떤 요청을 수정해야 하는지 질문한다. 503은 실습에서 용량 초과와 제공자 연결 실패를 모두 나타낼 수 있으므로 error.code를 함께 본다. 재시도 여부와 횟수는 전체 시간 예산과 중복 실행 위험을 기준으로 결정한다.

근거: https://www.rfc-editor.org/rfc/rfc9110.html, https://www.rfc-editor.org/rfc/rfc6585.html, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 22. 요청 ID와 원문 없는 추적

요청 수신 · ID 발급

처리 결과 · 상태·시간

최근 기록 · 최대 200건

원인 확인 · 코드·버전

강의 포인트: 메시지·답변·연락처는 기록하지 않음 · 메모리 캐시의 답변 보유는 별도

request_id는 서버가 발급하며 사용자 입력을 그대로 로그 키로 사용하지 않는다. 최근200건의 상태·시간·캐시 여부만 메모리에 보관한다. 실제 운영의 로그 접근권한·보존기간·다중 프로세스 수집은 추가 설계가 필요하다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 23. 동시 요청과 실패 복구

기다리는 작업과 계산하는 작업의 차이

요청 유입·처리 용량·시간 예산의 분리

다음 실험에서 확인할 경계와 성공·실패 조건을 살펴본다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 24. 순차 대기와 동시 대기



강의 포인트: 30ms 대기 4건의 개념도 · 실제 GPU 계산 속도와 무관

순차 대기는 4개의 30ms 작업을 연속 수행하므로 개념상 약120ms이고 동시 대기는 대기를 겹친다. 실제 측정은 스케줄링 오버헤드를 포함한다. 수면 모사로 GPU 연산 개선을 주장하지 않는다.

근거: https://fastapi.tiangolo.com/async/, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 25. 비동기 I/O 실행

async def io_job():

    await asyncio.sleep(0.03)

    return "done"



results = await asyncio.gather(

    *(io_job() for _ in range(4)))

강의 포인트: I/O · Input/Output · 입출력 / ASGI · Asynchronous Server Gateway Interface

코루틴을 만들기만 하면 실행이 완료되는 것은 아니다. await하거나 task로 예약해야 한다. await 지점에서 대기를 양보하는 성질과 여러 CPU 코어에서 계산을 병렬 수행하는 성질을 구분한다.

근거: https://fastapi.tiangolo.com/async/

## 26. async def와 블로킹 호출

협력 가능한 대기 · await client.post(...) · I/O 대기 중 다른 요청 진행

이벤트 루프를 막는 호출 · time.sleep(...) · 동기 HTTP 호출 · async def 안이라고 자동 비동기 아님

async def 내부의 동기 sleep이나 동기 HTTP 호출은 이벤트 루프를 막을 수 있다. 네트워크 I/O는 비동기 클라이언트를 사용하고 기존 동기 I/O는 제한된 스레드 실행을 검토한다. 무제한 스레드는 별도의 용량 문제를 만든다.

근거: https://fastapi.tiangolo.com/async/, https://docs.python.org/3.11/library/asyncio-task.html

## 27. 작업 성격과 실행 위치

작업 · 예시 · 선택 검토

I/O 대기 · 외부 HTTP·저장소 · 비동기 클라이언트

동기 I/O · 기존 동기 라이브러리 · 제한된 스레드

CPU 계산 · Python 중심 반복 계산 · 프로세스·별도 작업자

GPU 추론 · 언어 모델 실행 · 모델 서버·스케줄러

강의 포인트: CPU · Central Processing Unit / GPU · Graphics Processing Unit

워크로드에 맞는 실행 위치를 선택한다. Python 중심 CPU 계산은 프로세스 분리 비용을, GPU 추론은 모델 메모리와 스케줄링을 함께 본다. API 작업자 수와 모델 복제 수는 같은 숫자가 아니다.

근거: https://fastapi.tiangolo.com/async/, https://docs.python.org/3.11/library/asyncio-task.html

## 28. CPython 3.11과 GIL

GIL · Global Interpreter Lock · 전역 인터프리터 잠금

일반 Python 바이트코드의 스레드 병렬 실행에 제약

I/O·네이티브 연산·별도 프로세스는 조건을 나누어 검토

강의 포인트: 이 강좌 환경은 CPython 3.11 · 다른 런타임·버전의 조건을 혼합하지 않음

공통 실습의 CPython3.11을 기준으로 설명한다. GIL을 이유로 I/O 동시성이 불가능하다고 말하지 않는다. 네이티브 수치 라이브러리와 GPU 실행은 잠금 해제·장치 실행 조건이 달라 Python 반복문의 결과를 그대로 일반화하지 않는다.

근거: https://docs.python.org/3.11/glossary.html#term-global-interpreter-lock

## 29. 처리 용량과 즉시 거절



강의 포인트: max_inflight=2 · 무제한 대기열 없음 · 빈도 초과는 별도 429

active 검사는 단일 이벤트 루프에서 await 없는 구간으로 수행한다. 다른 프로세스·스레드에 공유되지 않는다. 요청 빈도 검사는 active 검사보다 먼저 수행하므로 용량 거절도 유입 토큰을 소비한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 30. 빈도 제한과 동시 처리 제한

빈도 제한 · 429 · 일정 시간에 들어오는 요청 제어 · 토큰 버킷의 보충률·burst

동시 처리 제한 · 503 · 실행 중인 작업 수 제어 · max_inflight · 종료 후 해제

빈도는 일정 시간에 유입되는 양이고 동시성은 현재 점유한 작업 수다. 짧은 burst를 허용해도 처리 중인 요청이 길면 active 한도에 먼저 도달할 수 있다. 이번 토큰 버킷은 사용자별 인증 제한이 아닌 전체 프로세스의 실험 장치다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 31. 클라이언트와 서버의 시간 예산

전체 요청 예산 ≥ 접속·대기·생성·전송

서버 제한시간과 클라이언트 대기시간을 각각 명시

외부 작업 취소는 별도의 확인 대상

강의 포인트: MOCK 기본 제한 0.3초 · 실제 Ollama 경로는 30초 · 서비스 목표값 아님

서버의 전체 제한시간과 HTTP 클라이언트의 접속·읽기·쓰기·풀 대기 제한은 서로 다른 경계다. 서버가 대기를 끝냈다고 외부 모델의 작업이나 과금도 종료됐다고 단정하지 않는다.

근거: https://www.python-httpx.org/advanced/timeouts/, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 32. 제한시간과 자원 해제

try:

    async with asyncio.timeout(self.settings.timeout_s):

        output = await self.generate(req)

except TimeoutError:

    # 504 오류 계약

    ...

finally:

    self.active -= 1

강의 포인트: 서비스 메서드의 개념 발췌 · 정상·오류·취소 모두 해제 · 전체 함수는 service.py

finally는 정상·상류 오류·시간 초과·코루틴 취소 모두에서 로컬 용량을 돌려주는 지점이다. 예제 발췌는 실제 service.py 구조의 요점을 보여주며 클래스 메서드의 인자명까지 동일한 복사 실행 코드는 아니다.

근거: https://docs.python.org/3.11/library/asyncio-task.html, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 33. 시간 초과의 실제 화면

선택 조건 · MOCK 제한시간 초과

확인 결과 · 504 · deadline_exceeded

복구 확인 · active=0 후 다음 요청

강의 포인트: 실행 캡처 · 정상값으로 오류를 숨기지 않는 계약

시간 초과 시뮬레이션은 서버 설정의 두 배를 기다려 deadline을 넘기게 한다. 성공 캐시가 있더라도 장애 주입은 캐시를 우회하므로 오류를 관찰할 수 있다. 실패 이후 /lab/stats의 active=0과 후속 요청을 함께 확인한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 34. 재시도 정책의 검토

상황 · 검토 · 금지할 동작

422 · 입력 수정 · 같은 입력 무한 반복

429·503 · 안내·백오프·횟수 상한 · 즉시 반복으로 부하 증폭

504 · 중복 실행·과금·취소 · 원래 작업 종료로 단정

스트림 중단 · 부분 답변·완료 상태 · 이어 붙여 완성으로 표시

강의 포인트: 이번 앱은 자동 재시도 미구현 · 재시도는 비용·중복·시간 예산과 함께 결정

즉시 무한 재시도는 과부하를 더 키운다. 지수 백오프·임의 분산·횟수 상한도 원래 작업의 중복 실행 위험을 없애지는 못한다. 이 앱은 재시도를 자동으로 넣지 않고 판단할 조건을 먼저 남긴다.

근거: https://www.rfc-editor.org/rfc/rfc9110.html, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 35. 취소 이후의 용량 검사

task = asyncio.create_task(service.chat(req, "cancel-demo"))

await asyncio.sleep(0.001)

task.cancel()

try:

    await task

except asyncio.CancelledError:

    pass

assert service.active == 0

강의 포인트: Notebook 02 · 로컬 자원 해제와 외부 GPU 작업 종료를 구분

클라이언트 단절·코루틴 취소·서버 제한시간은 별개다. 로컬 finally가 실행되어도 외부 제공자의 GPU 작업이나 과금 종료를 보장하지 않는다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 36. 캐시와 추론 구조

응답 재사용과 모델 내부 상태 재사용의 차이

빠른 응답의 원인과 재사용 가능한 범위

다음 실험에서 확인할 경계와 성공·실패 조건을 살펴본다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 37. 세 종류의 캐시

구분 · 재사용 대상 · 무효화 조건

응답 캐시 · 완성된 답변 · 입력·버전·권한 변경

검색 캐시 · 검색 결과·문서 조각 · 자료·권한·검색 설정 변경

KV 캐시 · Attention의 Key·Value · 모델·토큰·위치 변경

강의 포인트: KV · Key–Value · 세 캐시는 별도 계층 · 이번 앱은 응답 캐시만 구현

응답 캐시는 최종 문자열을, 검색 캐시는 문서 후보를, KV 캐시는 모델 내부 attention 상태를 재사용한다. 무엇을 저장하고 어떤 조건에서 재사용을 중단할지가 다르다. 실습의 TTLCache를 KV 캐시 구현이라고 소개하지 않는다.

근거: https://arxiv.org/abs/2309.06180, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 38. 같은 질문의 두 번째 요청



강의 포인트: 키 일치와 만료 확인 후 재사용 · 캐시 적중은 새 모델 추론이 아님

같은 키이고 아직 만료되지 않은 완료 결과만 적중한다. 적중해도 새 요청 ID를 발급하고 cached=true로 표시한다. 캐시 적중률이 높더라도 오래되거나 권한이 맞지 않는 답변이면 서비스 품질은 나빠질 수 있다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 39. 재사용 경계가 포함된 키

payload = {"message": req.message,

           "max_tokens": req.max_tokens,

           "provider": cfg.provider, "model": cfg.model,

           "prompt_version": cfg.prompt_version,

           "schema": "v1"}

key = sha256(canonical_json(payload)).hexdigest()

강의 포인트: 개념 발췌 · 실제 함수 cache_key · 인증·문서 권한이 있는 서비스는 그 경계도 포함

해시는 암호화가 아니다. 예제 키에는 원문 자체 대신 해시를 사용하지만 메모리 캐시는 답변을 저장한다. 사용자 식별자를 클라이언트가 보내는 값만으로 권한 경계로 믿지 않는다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 40. 권한과 버전 누락의 반례

직원용 문서를 참고한 답변이 같은 질문의 캐시에 저장

일반 사용자의 질문에 그 캐시가 재사용되는 위험

인증된 권한·문서 버전 경계부터 설계

강의 포인트: 설계 반례 · 현재 실습에는 인증·다중 tenant·문서 검색이 없음

직원과 일반 사용자라는 동일 질문의 권한 반례다. 다중 사용자 서비스는 인증된 신원·접근 가능 문서·버전을 생성과 캐시 경계에 결합해야 한다. 민감 문서의 존재 자체가 검색 결과나 로그에 드러나는 경로도 검토한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 41. 만료와 메모리 상한

TTL · Time To Live · 시간 경과 후 재사용 중단 · 기본 30초 · 단조 시계

LRU · Least Recently Used · 최근 사용하지 않은 항목부터 제거 · 최대 128항목 · 재시작 시 초기화

TTL은 최신성 정책의 일부이고 LRU는 메모리 용량 정책이다. 단조 시계를 사용해 시스템 시간 조정의 영향을 줄인다. 만료 항목은 조회 또는 용량 제거 시 정리되며 별도 청소 프로세스와 영구 저장소는 없다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 42. 가짜 시계로 확인하는 만료

clock = [0.0]

cache = TTLCache(2, 2, clock=lambda: clock[0])

cache.set("A", "version1")

clock[0] = 2.0

assert cache.get("A") is None

강의 포인트: Notebook 03 · 오래 기다리지 않고 만료 경계·용량 제거를 재현

시계를 함수로 주입하면 실제로2초를 기다리지 않고 만료 직전·정확한 만료 시각·이후를 검사할 수 있다. 의존성 주입은 모델 연결뿐 아니라 시간과 전송을 재현하는 작은 설계에도 유용하다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 43. 콜드 캐시의 중복 요청

요청 A · 캐시 없음 · 제공자 호출 · 캐시 저장

요청 B · 캐시 없음 · 제공자 호출 · 캐시 저장

강의 포인트: 동시에 시작하면 두 호출 모두 실행 가능 · 진행 작업 병합은 별도 기능

캐시 적중은 완료된 값에 대해서만 일어난다. 같은 콜드 키의 동시 요청은 두 번 제공자를 호출한다. 개선하려면 키별 진행 작업 병합과 취소·실패·한도 정책을 따로 설계해야 한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 44. 입력 처리와 순차 생성

Prefill · 입력 처리 · 입력 토큰의 상태 계산 · 길이·배치·모델·장치에 영향

Decode · 순차 생성 · 이전 토큰을 참고해 다음 토큰 생성 · 응답 길이·메모리·스케줄링에 영향

입력 처리와 생성 단계를 분리하면 긴 질문과 긴 답변이 서로 다른 병목을 만들 수 있음을 설명하기 쉽다. 실제 장치·모델·배치에 따라 계산 및 메모리 병목이 달라지며 단정적인 속도 비율을 제시하지 않는다.

근거: https://arxiv.org/abs/2309.06180

## 45. PagedAttention의 블록 참조

Key·Value · 토큰별 Key·Value

비연속 블록 · 비연속 블록의 참조

수업 범위 · GPU 성능 검증 제외

강의 포인트: Kwon et al., SOSP 2023, Figure 5 · CC BY 4.0 · 흑백 발췌

PagedAttention은 연속한 논리 토큰의 KV를 반드시 물리적으로 연속한 메모리에 보관하지 않도록 블록 기반 참조를 사용한다. Figure5는 구조 이해용이며 논문 성능 수치를 강좌 실습의 결과로 전이하지 않는다.

근거: https://arxiv.org/abs/2309.06180

## 46. vLLM의 작업자와 캐시 관리

스케줄러 · 요청 실행의 조정

캐시 관리자 · 블록 할당과 해제

API와 구분 · 추론 엔진 내부 구조

강의 포인트: Kwon et al., Figure 4 · CC BY 4.0 · 흑백 발췌 · 배포 성능 보장 아님

Figure4에서 API가 아닌 추론 엔진 내부의 스케줄러·캐시 관리자·작업자 역할을 구분한다. 이 도식만 보고 GPU 한 대의 최적 배치나 현재 vLLM 설치 호환성을 결정할 수는 없다.

근거: https://arxiv.org/abs/2309.06180

## 47. 동시 API 요청과 추론 배칭

API 동시성 · 여러 요청이 I/O 대기를 공유 · MOCK의 asyncio 실험 대상

모델 배칭 · 여러 시퀀스를 추론 엔진에서 스케줄 · 메모리·토큰·장치에 따른 별도 검증

API 동시성은 기다리는 여러 요청을 다루는 앱 구조이고 추론 배칭은 모델 실행의 스케줄링이다. asyncio.sleep 실험은 전자를 보여주지만 후자의 효율이나 모델 처리량을 측정하지 않는다.

근거: https://fastapi.tiangolo.com/async/, https://arxiv.org/abs/2309.06180

## 48. 추론 개선의 조건

선택 · 기대 효과 · 같이 볼 조건

출력 길이 제한 · 생성 작업 감소 · 답변 완전성·중단 이유

양자화 · 가중치 저장량 감소 · 품질·커널·장치

응답 캐시 · 반복 호출 감소 · 최신성·권한·유효성

추론 배칭 · 장치 활용·처리량 · 대기·메모리·개별 지연

강의 포인트: 특정 기법의 보편적 속도 우위를 가정하지 않음 · 실제 제공자 환경에서 비교

출력 길이를 줄이면 필요한 정보가 누락될 수 있고 양자화로 저장량을 줄여도 특정 커널에서 더 빠르다는 보장은 없다. 품질·지연·처리량·메모리·비용을 같은 조건으로 비교하고 한 지표의 개선을 전체 성공으로 소개하지 않는다.

근거: https://arxiv.org/abs/2309.06180, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 49. 스트리밍과 완료 상태

첫 바이트·첫 내용·완료 시점의 분리

부분 답변과 실패·중단의 명시적 처리

다음 실험에서 확인할 경계와 성공·실패 조건을 살펴본다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 50. SSE 이벤트의 진행



강의 포인트: SSE · Server-Sent Events · 서버가 보내는 단방향 이벤트 · POST는 fetch 사용

기본 브라우저 EventSource는 GET 기반이다. 본 실습은 POST 요청 본문을 보내므로 fetch Response.body를 읽고 빈 줄 단위 SSE 이벤트를 파싱한다. meta는 첫 토큰이 아니다.

근거: https://html.spec.whatwg.org/multipage/server-sent-events.html, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 51. 빈 줄로 구분하는 이벤트

event: meta

data: {"request_id":"...","simulated":true}



event: delta

data: {"text":"첫 내용 조각"}



event: done

data: {"complete":true}

강의 포인트: UTF-8 · text/event-stream · 네트워크 청크와 이벤트 프레임 경계는 다를 수 있음

네트워크에서 한 번 읽은 바이트 묶음이 한 이벤트와 같지 않을 수 있다. UTF-8 디코더 상태와 남은 문자열을 유지한 뒤 빈 줄이 나올 때 프레임을 파싱한다. 예제 서버는 event와 JSON data를 함께 보낸다.

근거: https://html.spec.whatwg.org/multipage/server-sent-events.html

## 52. 브라우저의 스트림 수신

메타와 내용 · 첫 delta에서 내용 시간 측정

완료 조건 · done 수신 여부

중단 동작 · 수신 중단·서버 용량 해제

강의 포인트: 실제 로컬 캡처 · 내용은 MOCK 문자 조각 · 토큰 생성 속도 아님

브라우저 화면의 first_delta_ms는 최초 내용 이벤트가 도착한 시각이다. 메타데이터가 먼저 도착해도 내용 시간으로 세지 않는다. 일반 응답과 달리 이 경로는 캐시를 사용하지 않고 MOCK 전용이다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 53. HTTP 200과 스트림 성공

응답 시작 전 · 입력·용량 검증 가능 · 422·503 등 상태 코드 결정

응답 시작 후 · 상태를 504로 바꿀 수 없음 · error 이벤트·미완료 상태로 전달

StreamingResponse가 헤더를 보낸 뒤에는 이미 전송한 HTTP 상태를 새 오류 코드로 교체할 수 없다. 오류 이벤트를 전송하거나 연결이 끝날 수 있으므로 클라이언트가 완료 마커와 미완료 상태를 구분해야 한다.

근거: https://html.spec.whatwg.org/multipage/server-sent-events.html, https://fastapi.tiangolo.com/advanced/custom-response/, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 54. 사용자가 보는 완료 상태

관측 · 판정 · 화면·저장

done 수신 · 완료 · 완료 표시·결과 저장

error 수신 · 실패·미완료 · 이유·다음 행동

done 없는 종료 · 중단·불확실 · 부분 답변 표시

수신 중단 · 사용자 취소 · 자원 해제 별도 확인

강의 포인트: 토큰 하나 수신했다고 전체 요청 성공으로 집계하지 않음

답변 일부가 유용하더라도 done이 없으면 완료 성공으로 저장하지 않는다. 사용자 중단, 네트워크 단절, 서버 오류를 UI에서 구분할 수 있는 최소 정보를 남긴다. 스트림 오류율은 일반 HTTP 상태만으로 집계하면 빠진다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 55. 첫 내용 조각과 전체 완료



강의 포인트: 로컬 TCP 실측 · ms · MOCK 문자 조각 · 실제 LLM TTFT와 구분

로컬 TCP에서 수신한 첫 내용 조각과 done까지의 시간을 비교한다. 네트워크 응답 크기나 앱의 고정 sleep에 좌우되는 교육용 측정이며 실제 모델 토큰 단위 성능은 아니다.

근거: repo:scripts/verify_week09_live.py, repo:week09/lab/service.py

## 56. TTFT와 스트림 측정의 경계

TTFT · Time To First Token · 첫 토큰까지의 시간

이번 MOCK은 첫 delta와 전체 완료 시간을 기록

ASGITransport는 버퍼링 가능하므로 TCP 실험에서 확인

강의 포인트: Notebook 04는 형식 검사 · scripts/verify_week09_live.py는 실제 로컬 TCP 검사

실제 TCP 검증은 별도 Uvicorn 프로세스를 임시 포트에 띄우고 HTTPX 스트림 수신 시간을 기록한다. 그래프는 첫 delta와 전체 완료의 실측값이며 모델 토큰 생성·인터넷 환경은 다루지 않는다.

근거: https://www.python-httpx.org/advanced/transports/, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 57. 단계별 실행과 부하 비교

예상·실행·변경·해석의 순서

성공 지연·오류율·성공 처리량의 동시 확인

다음 실험에서 확인할 경계와 성공·실패 조건을 살펴본다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 58. 다섯 Notebook의 역할

파일 · 실험 · 권장

01 API 계약 · 명세·정상·422·추적 · 15분

02 비동기·복구 · 503·504·502·429·취소 · 20분

03 캐시·버전 · 적중·키·TTL·중복 호출 · 15분

04 스트리밍 · 프레임·done·error·중단 · 15분

05 부하·프로젝트 · 성공 지연·오류율·요구사항 · 20분

강의 포인트: 각 파일 독립 실행 · 총 111셀·코드 53셀 · 수업은 핵심 셀 선택

각 Notebook은 새 앱을 만들어 다른 파일의 실행 순서에 의존하지 않는다. 전체 실행은85분 권장이고 수업은 선택 셀로40분 정도를 진행한다. 실제 셀 실행 시간보다 예상·변경·해석의 토론 시간이 중요하다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 59. VS Code 환경과 커널

# 저장소 루트에서 기존 환경 활성화

source .venv/bin/activate

python -m pip install -r requirements.txt

python -m pytest -q week09/lab/tests

code .

강의 포인트: 처음 설치: python3.11 -m venv .venv · Windows 활성화는 실습 README 참조

기존 .venv가 있으면 재생성하지 않는다. 설치와 실행은 동일한 Python3.11 환경에서 수행한다. 필수 실습에 Locust·Redis·GPU 패키지를 추가하지 않으며 공통 requirements는 변경하지 않는다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 60. VS Code의 실행 순서

저장소 루트 · llmops-16week 폴더 전체 열기

커널 선택 · Python Environments · .venv / Python 3.11

순차 실행 · 위에서 아래로 실행 후 변수 하나 변경

강의 포인트: Notebook 자동 실행은 앱 소스나 requirements를 덮어쓰지 않음

커널이 다른 Python이면 import가 되더라도 패키지 동작이 달라질 수 있다. 파일 하나가 아닌 저장소 루트를 열어 week09 패키지와 공통 모듈 경로를 함께 인식시킨다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 61. 브라우저 실습 서버

python -m uvicorn week09.lab.app:app \

  --host 127.0.0.1 --port 8009



# 브라우저

http://127.0.0.1:8009/

http://127.0.0.1:8009/docs

강의 포인트: 한 worker · 외부 공개 금지 · 포트 충돌 시 8019로 변경 · 종료 Ctrl+C

127.0.0.1에만 바인딩하고 한 worker를 사용한다. 이 앱은 인증이 없고 교육용 장애 주입을 제공하므로 공용 IP로 공개하지 않는다. 다른 수업 서버를 임의로 종료하지 말고 자신의 포트를 변경한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 62. 40분 핵심 실습의 선택

계약 · 01 정상·422

복구 · 02 한도·초과

재사용 · 03 적중·중복

완료 · 04 error·중단

강의 포인트: 남은 시간에 05 결과 해석 · 전체 Notebook은 복습에서 확장

01의 정상·공백 검사,02의 동시 한도·시간 초과,03의 캐시 적중과 중복,04의 done·error를 우선한다. 05의 부하 결과는 함께 읽고 전체 실행·선택 제공자 연결은 복습에서 확장한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 63. 부하 실험의 실행 조건

report = await run_load(

    client, n=24, concurrency=2,

    use_cache=False, warmup=2)

display(report["summary"])

강의 포인트: Notebook 05 · 동시 요청 1·2·6 비교 · 처리 용량 2 · 수면 30ms · 캐시 OFF

run_load는 동시 진행 수를 semaphore로 제한하고 매 실행 최대100건·동시성8로 제한한다. warmup 요청은 요약에서 제외한다. 응답이 끝나면 다음 요청이 진행되므로 고정 도착률 시험과 다르다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 64. 동시 요청 기반 부하

Closed-loop · 응답 후 다음 요청을 진행하는 부하

응답이 느리면 클라이언트의 다음 요청 유입도 줄어듦

고정 도착률·운영 트래픽·장시간 안정성은 별도 시험

강의 포인트: 이번 실험은 최대 100요청·동시성 8 · 외부 서비스 부하테스트 금지

폐쇄형 클라이언트에서는 지연이 늘면 다음 요청의 발행도 늦어진다. 운영의 급격한 유입이나 대기열 증가를 충분히 재현하지 못할 수 있다. 외부 API나 타인의 서버에 이 코드를 무단 적용하지 않는다.

근거: repo:week09/lab/benchmark.py

## 65. 동시 요청과 오류율



강의 포인트: 실행별 24요청 · 처리 용량 2 · 성공과 거절을 합쳐 분모 계산 · ASGI MOCK

동시성1과2는 각24건이 성공한다. 동시성6은 처리 한도2를 초과해 빠른503이 발생할 수 있다. 폐쇄형 단기 시험의 특성으로 오류 건수와 시간은 실행마다 달라진다.

근거: repo:week09/lab/benchmark.py, repo:week09/lab/notebooks/05_load_and_project.ipynb

## 66. 빠른 오류가 만드는 평균 착시

가상 요청 · 건수 · 시간

성공 · 1 · 100ms

503 거절 · 9 · 각 1ms

전체 평균 · 10건 · 10.9ms

성공 p50 / 오류율 · 성공만 / 전체 · 100ms / 90%

강의 포인트: 계산 설명용 합성 값 · 거절이 빠르다고 서비스가 좋아진 것은 아님

가상값의 전체 평균은 (100+9×1)/10=10.9ms다. 성공 응답은100ms이며 오류율은90%다. 평균만 보면 빠르지만 대부분 요청을 거절했다는 중요한 사실이 사라진다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 67. 성공 요청의 지연 분포



강의 포인트: n은 성공 표본 수 · p50·p95 · ms · 거절은 오류율로 별도 확인

분포에는 성공 응답만 포함한다. 실패율과 전체 표본은 다른 장표에서 함께 보고한다. 성공 표본이 없는 경우 지연을0으로 기록하지 않고 None으로 남겨 측정 불가능을 표현한다.

근거: repo:week09/lab/benchmark.py, repo:week09/lab/notebooks/05_load_and_project.ipynb

## 68. 분위수와 표본 수

p95 · 관측값의 95백분위 지점

모든 요청이 95ms라는 의미도, 95%의 성공률도 아님

소수 표본의 p99로 장시간 서비스 목표를 보장하지 않음

강의 포인트: 실습은 NumPy percentile · linear 보간 · 실패율은 별도 분모

백분위수 보간 방법과 성공만 포함하는 필터를 명시한다. 작은 표본에서 p99는 극단값 몇 개에 크게 좌우되므로 운영 보장이나 SLA로 제시하지 않는다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 69. 성공 처리량과 완료 처리량



강의 포인트: 성공 요청/s · 전체 완료 요청/s를 구분 · 빠른 거절은 성공 처리량에 포함하지 않음

전체 완료 처리량은 성공과 빠른 오류를 모두 세고 성공 처리량은200 응답만 센다. 같은 단위인 요청/초라도 분자의 의미가 다르다. 스트리밍은 done까지 확인하는 별도의 성공 정의가 필요하다.

근거: repo:week09/lab/benchmark.py, repo:week09/lab/notebooks/05_load_and_project.ipynb

## 70. 성능 지표와 서비스 목표

SLI · 서비스 지표 · Service Level Indicator · 성공률·지연·완료 여부

SLO · 서비스 목표 · Service Level Objective · 지표의 목표·기간·대상 정의

강의 포인트: SLA · Service Level Agreement · 계약·책임의 합의 · 이번 실험은 SLA가 아님

SLI는 측정값, SLO는 대상·기간·목표를 포함한 운영 목표, SLA는 계약과 책임의 합의다. 단기 로컬 실험의 p95를 장기 목표 달성이나 계약 보장으로 바꾸어 쓰지 않는다.

근거: https://sre.google/sre-book/service-level-objectives/

## 71. 캐시 적중과 비적중의 비교



강의 포인트: 성공 p50 · ms · 동시성 2 · 워밍업 제외 · 캐시 적중을 모델 속도로 해석하지 않음

캐시 적중 조건에서는 워밍업에서 만든 답변을 재사용해 제공자 호출이1회다. 캐시 OFF와 비교한 지연 개선을 모델 자체의 추론 최적화라고 쓰면 안 된다. 실제 서비스에서는 반복 질의 비율과 권한·만료 조건을 함께 측정한다.

근거: repo:week09/lab/benchmark.py, repo:week09/lab/notebooks/05_load_and_project.ipynb

## 72. 결과와 함께 남길 실행 조건

구분 · 기록

환경 · Python·패키지·기기·프로세스 수

입력 · 표본 수·길이·출력 제한·질의 구성

캐시 · 콜드·워밍업·적중·만료

부하 · 동시성·도착 방식·실행 시간

결과 · 성공 지연·오류율·성공 처리량·한계

강의 포인트: 결과 JSON은 로컬 output/validation/week09-lab/ · 공개 제출 원문과 분리

환경·입력 길이·표본·동시성·캐시·워밍업·실행 시간을 결과와 함께 저장한다. 파일은 로컬 output/validation에 남고 공개 자료에 개인 입력이나 학생 제출물을 포함하지 않는다. 수치가 달라지면 원인을 먼저 확인한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 73. 프로젝트 적용과 선택 확장

요구사항·API·시험·실패 처리의 연결

실제 모델 연결은 공통 경로 이후의 선택

다음 실험에서 확인할 경계와 성공·실패 조건을 살펴본다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 74. 기획서 요구사항의 실행 연결

항목 · 시험 · 실패 처리

FR01 · 근거 안내 · 정상·근거 부족 사례 · 검토 안내

FR02 · 구조화 응답 · 필드·타입·경계 검사 · 입력 수정·재시도 제한

NFR01 · 서비스 품질 · 지연·오류·완료를 같이 확인 · 용량·시간·복구 조정

강의 포인트: FR · Functional Requirement / NFR · Non-Functional Requirement · 목표값은 제안 단계

기능 요구사항과 비기능 요구사항에 각각 확인 방법과 실패 처리를 연결한다. 문서에 적은 응답 목표는 실제 비교 실험 이전에는 제안값이다. 평균 지연 하나보다 성공·실패·완료·자원 복구의 증거가 먼저다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 75. Ollama 선택 경로의 사전 점검

설치 확인 · ollama list · 정확한 모델 태그

서버 확인 · 127.0.0.1:11434 · /api/tags

생성 확인 · think:false · 출력 제한 · 타임아웃

강의 포인트: 모델·서버 버전에 따라 thinking 지원 다름 · 실제 모델 속도는 기기에서 확인

ollama list로 설치된 정확한 태그를 확인한다. 404는 경로·버전·모델명 등 원인을 나누어 확인하고 모델 다운로드를 자동 실행하지 않는다. think:false의 지원과 실제 응답은 선택 모델에서 확인해야 한다.

근거: https://docs.ollama.com/api/chat, https://docs.ollama.com/capabilities/thinking

## 76. 실제 모델 연결의 명시적 설정

# 기존 MOCK 서버 종료 후 별도 터미널

export WEEK09_PROVIDER=ollama

export WEEK09_MODEL="설치된_정확한_모델_태그"

python -m uvicorn week09.lab.app:app \

  --host 127.0.0.1 --port 8009

강의 포인트: 예시 태그를 그대로 쓰지 않음 · /ready 확인 · 실제 모델 스트리밍은 이번 앱에서 미지원

이 설정은 학생이 명시적으로 선택한 로컬 제공자만 사용한다. 실습의 기본 경로에서는 실제 Ollama를 호출하지 않는다. /ready는 설치 확인이고 생성·품질·thinking 동작은 별도 확인한다.

근거: https://docs.ollama.com/api/chat, repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 77. 공통 실습과 선택 모델의 경계

검증된 공통 경로 · MOCK·5개 Notebook·계약·복구 · ASGI·실제 TCP·브라우저 실행

선택 Ollama 경로 · 어댑터 계약은 모의 전송으로 검사 · 실제 속도·품질은 기기에서 재확인

공통 경로는 외부 모델이 없어도 모두 실행할 수 있다. Ollama 어댑터는 모의 HTTP 전송으로 정상·누락 모델·연결 실패 계약을 검사했으며 실제 모델의 속도·메모리·출력 품질은 이 결과에 포함되지 않는다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 78. 최소 기능 한 개의 설계 리뷰

사용 가치 · 누구의 어느 요청을 처리하는가

검증 근거 · 성공·오류·취소를 재현할 수 있는가

운영 경계 · 권한·자료·비용·복구 중 빠진 것은 무엇인가

강의 포인트: 다음 주: 배포 구조·실행 관찰·복구 · 새 과제 기한은 소속 공지 기준

교수 리뷰에서는 어떤 모델을 썼는지보다 요구사항 하나가 실제로 동작하는지와 실패 이후 사용자에게 어떤 선택을 주는지 확인한다. 다음 주 배포 단원으로 넘어가기 전에 실행 명령·대표 입력·알려진 한계를 남긴다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 79. 구현 범위와 남은 운영 위험

현재 구현 · 입력·출력·오류·단일 프로세스 한도 · 로컬 실험·자원 해제·완료 계약

배포 전 추가 작업 · 인증·권한·요청 본문 크기·암호화 · 외부 저장·다중 worker·취소·관측

이 앱을 그대로 운영 배포하지 않는다. 인증·권한·전체 요청 크기 제한·암호화·영속 저장·다중 worker 상태·실제 제공자 취소·중앙 지표가 남은 작업이다. 구현하지 않은 기능은 시연에서 명확히 표시한다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md

## 80. 참고 자료와 재현 경로

자료 · 출처·실행

FastAPI · fastapi.tiangolo.com · 요청·응답·async

HTTP·SSE · RFC 9110 · WHATWG HTML

PagedAttention · arxiv.org/abs/2309.06180 · Figure 4·5

실습 코드 · week09/lab/ · notebooks/01–05

출처·한계 · week09/lecture/assets/SOURCES.md

강의 포인트: 2025 실습의 주제 계승 · 공통 환경·실패 복구·개인정보 경계를 재설계

FastAPI와 HTTPX는 고정된 강좌 패키지에서 실행하고 공식 문서는 개념과 API 의미를 확인하는 데 사용했다. 논문 Figure4·5는2023년 구조 설명용이며 현재 제품의 설치·성능·우위를 대신하지 않는다.

근거: repo:week09/lab/service.py, repo:week09/lab/app.py, repo:curriculum/2026-2/00_운영_커리큘럼.md