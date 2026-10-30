# 9주차 출처·이미지·실험 경계

확인일: 2026-10-30. 원문·공식 문서를 우선했으며 소프트웨어 실행은 강좌의 고정 패키지를 사용한다. 최신 문서에 새로 추가된 기능이 고정 버전에서 모두 지원된다고 가정하지 않는다.

## 외부 원본 이미지

Kwon et al., **Efficient Memory Management for Large Language Model Serving with PagedAttention**, SOSP2023, [arXiv:2309.06180v1](https://arxiv.org/abs/2309.06180v1), [PDF](https://arxiv.org/pdf/2309.06180).

- `vllm-system-figure4.png`: 원문5쪽 Figure4의 그림 영역,300dpi 흑백 발췌. API와 추론 엔진 내부의 역할 차이를 설명한다.
- `pagedattention-figure5.png`: 원문5쪽 Figure5의 그림 영역,300dpi 흑백 발췌. Key·Value 상태의 비연속 블록 참조를 설명한다.
- 원문 arXiv 라이선스 링크는 [CC BY4.0](https://creativecommons.org/licenses/by/4.0/)다. 변경은 그림 영역 발췌와 흑백 변환이며 도식의 문자·화살표·비율을 다시 그리지 않았다. 저자가 이 강좌를 보증한다는 의미가 아니다.
- 논문 속 GPU·모델·데이터 조건을 다른 기기나 현재 제품 성능으로 일반화하지 않는다. 성능 배수는 이 강좌의 실험 결과로 인용하지 않았다.

## 자체 실행 캡처

`lab-success.jpg`, `lab-timeout.jpg`, `lab-stream.jpg`는 `week09/lab/index.html`과 `app.py`의 실제 로컬 브라우저 실행 화면이다. 합성 질문·MOCK 고정 응답만 사용했다. 표시된 request_id는 무작위 실행 식별자이며 학생 정보가 아니다. 원문과 결과의 의미를 바꾼 합성 UI나 가짜 모델 평가 화면이 아니다.

## 공식 기술 문서

- [FastAPI 요청 본문](https://fastapi.tiangolo.com/tutorial/body/), [응답 모델](https://fastapi.tiangolo.com/tutorial/response-model/), [오류 처리](https://fastapi.tiangolo.com/tutorial/handling-errors/).
- [FastAPI 동시성과 async](https://fastapi.tiangolo.com/async/), [StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/).
- [Python3.11 asyncio 작업·취소·타임아웃·스레드](https://docs.python.org/3.11/library/asyncio-task.html), [GIL](https://docs.python.org/3.11/glossary.html#term-global-interpreter-lock).
- [HTTPX ASGITransport·모의 전송](https://www.python-httpx.org/advanced/transports/), [timeout 구분](https://www.python-httpx.org/advanced/timeouts/).
- [RFC9110 HTTP 의미](https://www.rfc-editor.org/rfc/rfc9110.html), [RFC6585 429](https://www.rfc-editor.org/rfc/rfc6585.html).
- [WHATWG Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html): UTF-8·event/data·빈 줄 프레임·EventSource.
- [Ollama chat API](https://docs.ollama.com/api/chat), [thinking](https://docs.ollama.com/capabilities/thinking): 실제 지원은 선택 모델·서버에서 확인.
- [Google SRE 서비스 수준 목표](https://sre.google/sre-book/service-level-objectives/): 지표·목표·합의의 구분.

## 차트의 재현 근거

- `week09/lab/notebooks/05_load_and_project.ipynb`와 `benchmark.py`가 로컬 `output/validation/week09-lab/benchmark-report.json`을 만든다.
- 기본 비교는24요청, 동시성1·2·6, 처리 용량2, 고정 수면30ms, 캐시 OFF, 워밍업2건 제외다. 성공 지연·오류율·성공/전체 완료 처리량을 나눈다.
- 캐시 비교는 동일 질문·동시성2·워밍업 후 적중 상태다. 모델 추론 속도 비교가 아니다.
- `scripts/verify_week09_live.py`가 실제 로컬 TCP에서 MOCK 문자 조각의 첫 delta와 전체 완료 시간을 측정하고 `output/validation/week09-live/receipt.json`을 만든다.
- 순차/동시 대기 개념도,10.9ms 평균 착시 사례는 설명용 합성 계산이다. 실측 차트와 구분한다.
- 실제 GPU·모델 품질·운영 트래픽·장시간 SLO는 검증하지 않는다. 검증 실행본·로그는 공개 수업 자료와 분리한다.

## 보존본과의 관계

`AS-IS 2025 2nd semester/`의9주차 통합 강의안·콘티·Notebook·앱은 주제 참고용이다. 원본 파일을 덮어쓰지 않았다. 새 Notebook은 런타임 소스 생성·requirements 덮어쓰기·숨은 외부 호출을 하지 않으며 상태와 실패의 계약을 검사한다.
