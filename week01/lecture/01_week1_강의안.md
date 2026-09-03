# Week 01 — LLM을 호출하는 것과 운영하는 것은 다르다

## 강의 정의

- 핵심 문장: 수강생은 “LLM을 한 번 호출하는 사람”이 아니라 응답을 기록·평가·재현·개선하는 운영자로 첫 주를 마친다.
- 기본 운영: 180분 워크숍(이론·대화 110분 + 준비 20분 + 실습·회고 50분)
- 압축 운영: AS-IS 기준 100분(슬라이드 1–3, 5–6, 9, 12–15, 19–23, 29–38 중심)
- 실습 서비스: `TRACE/01`, 기본 demo provider / 선택 Ollama provider
- 완료 조건: 같은 입력으로 비교 가능한 실행 2회 이상, trace 확인, 개선 판단 2문장

## 학습성과

수업을 마친 수강생은 다음을 할 수 있다.

1. AI → 딥러닝 → Transformer → LLM의 전환을 “다음 병목을 해결한 과정”으로 설명한다.
2. Prompt, Retrieval/Tool, SFT, RLHF/DPO, PEFT의 역할과 개입 비용을 구분한다.
3. DevOps, MLOps, LLMOps에서 운영 자산이 어떻게 확장되는지 설명한다.
4. LLM 서비스의 5단계 개선 순환을 자신의 서비스 사례에 매핑한다.
5. Python 3.11 환경에서 API를 실행하고 `prompt_version`, model, latency, token estimate, status가 포함된 trace를 확인한다.
6. 한 번에 변수 하나를 바꾼 실험으로 다음 개선 가설을 제시한다.

## 강사 소개 — 공개용 기준

> 차성재 | AI Product Manager · 서울시립대학교/아주대학교 AI 부문 겸임교수  
> 금융(AutoML·MLOps) → 의료(Computer Vision·DataOps) → 교육(LLMOps·AICC) → 커머스(Agentic AI)의 제품 개발·운영 경험  
> 대학원 정규 강의와 기업 대상 Prompt Engineering·LLM/RAG/LLMOps·AI Native 실습형 교육  
> AI를 데모가 아닌 문제정의·PRD·프로토타입·평가·워크플로우·운영 지표로 연결  
> 《딥러닝의 정석 2판》 역자 · Microsoft Certified: Azure AI Engineer Associate

공개 저장소에서는 현직 회사명·팀명·내부 프로젝트·내부 지표를 노출하지 않는다. 현직은 `대형 패션·라이프스타일 커머스 플랫폼의 AI Product Manager`로만 표현한다.

## 180분 운영표

| 시간 | 슬라이드 | 운영 | 현장 증거 |
|---:|---:|---|---|
| 00–10분 | 1–3 | 실패 응답 cold open, 오늘 목표 | “호출과 운영의 차이” 한 문장 |
| 10–22분 | 4–7 | 강사·과목·평가 계약 | 개인 관심 서비스 1개 |
| 22–42분 | 8–14 | 기준 사례, AI→Transformer→LLM | LLM이 보장하지 않는 것 1개 |
| 42–58분 | 15–19 | 개입 레버와 post-training | 사례에 적용할 첫 레버 |
| 58–68분 | — | 휴식·2인 토의 | 가장 위험한 실패 가설 |
| 68–90분 | 20–23 | Ops 진화와 5단계 lifecycle | 관리 자산 4개 |
| 90–110분 | 24–30 | 단계별 산출물과 16주 지도 | 사례의 5단계 매핑 |
| 110–120분 | 31–34 | 실습 DoD, preflight, baseline | 환경·서비스 health 확인 |
| 120–130분 | — | 휴식·모델 warm-up | 실패자는 demo provider로 전환 |
| 130–170분 | 35–37 | 요약·신호 추출·A/B 실험 | 비교 가능한 trace 2건 이상 |
| 170–180분 | 38 | 공유·exit ticket | 개선 판단 2문장 |

## 100분 압축 운영표

| 시간 | 슬라이드 | 운영 |
|---:|---:|---|
| 00–08분 | 1–3 | 문제와 목표 |
| 08–18분 | 5–6, 9 | 수업 구조와 LLMOps 필요성 |
| 18–33분 | 12–15, 19 | Transformer·LLM·개입 레버 |
| 33–48분 | 20–23 | Ops 진화와 lifecycle |
| 48–60분 | 29–34 | trace, 환경, baseline |
| 60–92분 | 35–37 | `TRACE/01` 실습 |
| 92–100분 | 38 | 비교·회고 |

## 38장 슬라이드 콘티

### A. Opening & Contract — 1–9

#### 1. LLM을 호출하는 것과 운영하는 것은 다르다

- 화면: 검은 바탕, 거대한 제목, 작은 `W01 / ORIENTATION & LIFECYCLE`
- 멘트: “오늘 모델 하나를 더 아는 것보다, 같은 결과를 다시 만들 수 있는 사람이 되는 것이 목표입니다.”

#### 2. 그럴듯한 오답이 오늘의 출발점이다

- 왼쪽: 맥락 없는 질문 `LLMOps 5단계를 알려줘.`
- 오른쪽: 강의 기준과 어긋난 그럴듯한 답
- 질문: “틀린 사실보다 더 위험한 것은 무엇인가?”
- 회수: 기준·맥락·버전·평가가 없으면 ‘틀렸다’고 판정할 수조차 없다.

#### 3. 오늘 목표는 첫 호출을 비교 가능한 실험으로 바꾸는 것이다

- 흐름: `CALL → TRACE → COMPARE → IMPROVE`
- 산출물: 실행 가능한 서비스, trace 2건, 개선 판단 2문장

#### 4. 강의자는 네 개 도메인에서 같은 운영 문제를 봤다

- 경력선: 금융 → 의료 → 교육 → 커머스
- 공통 질문: “정확한가?” 다음에 “재현·관찰·통제 가능한가?”
- 개인정보·현직 상세는 넣지 않는다.

#### 5. 이 과목의 산출물은 모델이 아니라 개선 루프다

- `Prompt / RAG / Fine-tuning / API / Eval / Safety / Cost`가 하나의 순환에 연결됨
- 한 주의 notebook을 다음 주가 재사용한다.

#### 6. 매주 만든 증거가 Capstone의 한 시스템이 된다

- 01–03: prompt·trace·eval
- 04–05: retrieval
- 06–07: adaptation
- 09–10: serving·observability
- 11–14: evaluation·agent·safety·cost
- 15–16: capstone·발표

#### 7. 평가는 실행보다 재현·비교·설명을 본다

- evidence: README, 실행 환경, config/version, 결과 로그, 비교와 판단
- 일정·점수 비율은 해당 학기 LMS를 canonical source로 사용한다.

#### 8. 오늘의 기준 사례는 ‘고객 피드백 도우미’다

- 입력: 고객 피드백
- 출력: 핵심 요약 / signal–friction–next action / 실무 문장
- 운영 증거: trace id, prompt version, provider/model, latency, token estimate, status

#### 9. 데모는 5분이지만 운영은 나머지 95%다

- 수면 위: prompt → model → answer
- 수면 아래: dataset, version, evaluation, timeout, fallback, safety, cost, ownership
- 현업 노하우: “좋은 데모를 보고 배포 결정을 내리지 않는다.”

### B. LLM & Intervention Levers — 10–19

#### 10. AI의 역사는 병목이 이동한 기록이다

- `RULE → DATA → COMPUTE → OPERATION`
- 연도 암기 대신, 각 전환이 무엇을 자동화했는지 묻는다.

#### 11. 데이터·GPU·딥러닝이 특징 설계를 학습으로 바꿨다

- 사람이 feature를 정하던 방식 → representation learning
- 한계: 학습 데이터와 목표가 잘못되면 규모는 문제를 증폭한다.

#### 12. Transformer는 token 사이의 관계를 한꺼번에 계산한다

- self-attention의 직관: “현재 token을 이해하기 위해 어느 token을 얼마나 볼 것인가”
- 병렬화와 장거리 의존성이라는 전환점만 남기고 구조 세부는 참고자료로 이동한다.

#### 13. LLM은 범용 능력을 주지만 업무 정답은 보장하지 않는다

- 가능: 생성, 요약, 변환, 분류, 코드
- 미보장: 사실성, 일관성, 최신성, 권한, 비용, 응답시간

#### 14. Pretraining 이후에도 제품 정의가 남는다

- 기반 모델은 다음 token 확률을 잘 맞추도록 학습된다.
- 제품은 누구에게 어떤 상황에서 무엇을 얼마나 잘해야 하는지 결정해야 한다.
- `MODEL CAPABILITY ≠ SERVICE RELIABILITY`

#### 15. 모델을 바꾸기 전에 네 개의 개입 레버를 구분한다

- Prompt: 지시·형식·예시
- Retrieval/Tool: 외부 지식·행동
- Fine-tuning: 반복되는 행동·도메인 적응
- Model routing: 품질·비용·지연 trade-off

#### 16. SFT는 좋은 입력–출력 예시로 행동을 가르친다

- instruction / input / ideal output triplet
- 적합: 반복되는 형식·말투·도메인 태스크
- 주의: 잘못된 예시를 더 일관되게 재현할 수도 있다.

#### 17. RLHF와 DPO는 선호를 배우지만 경로가 다르다

- RLHF: preference → reward model → policy optimization
- DPO: preference pair로 policy를 직접 최적화
- 둘을 같은 그림으로 뭉개지 않는다.

#### 18. LoRA·PEFT는 바꾸는 parameter를 줄여 실험 비용을 낮춘다

- base weight는 고정, 작은 adapter를 학습
- 이점: 저장·배포·실험 단위가 작아짐
- 판단 기준은 “가능한가”가 아니라 “prompt/RAG보다 이득인가”다.

#### 19. 가장 싸고 되돌리기 쉬운 레버부터 검증한다

- 기본 순서: baseline → prompt → retrieval/tool → routing → fine-tuning
- 예외: 규제·latency·on-device 등 제약이 순서를 바꿀 수 있음

### C. Ops & Lifecycle — 20–30

#### 20. DevOps→MLOps→LLMOps는 운영 자산이 늘어난 역사다

- DevOps: code, build, release, runtime
- MLOps 추가: data, feature, model, experiment
- LLMOps 추가: prompt, context, response, evaluation, feedback, guardrail

#### 21. LLM은 prompt·context·response·evaluation도 버전 자산으로 만든다

- `같은 코드 + 다른 prompt`도 다른 동작
- `같은 prompt + 다른 retrieved context`도 다른 동작
- trace는 이 조합을 한 번의 실행으로 묶는 ID다.

#### 22. LLMOps는 다섯 지표를 동시에 지킨다

- QUALITY · LATENCY · COST · SAFETY · REPRODUCIBILITY
- 현업 노하우: 한 축을 개선할 때 나머지 네 축의 regression을 확인한다.

#### 23. 다섯 단계는 선형 절차가 아니라 폐루프다

`기획·데이터 → 프롬프트·컨텍스트 → 실행·배포 → 평가·관찰 → 개선·버전`

- 마지막 단계는 다음 기획의 입력이다.
- 이번 학기 모든 주차를 이 그림에 다시 배치한다.

#### 24. 1단계 — 성공 조건과 데이터 경계를 먼저 고정한다

- 질문: 누구의 어떤 결정을 돕는가?
- 증거: representative input, expected behavior, 금지 조건, PII/license 경계

#### 25. 2단계 — 프롬프트를 코드처럼 버전·테스트한다

- prompt id/version, input/output schema, 예시, 변경 이유
- 눈으로 읽는 prompt보다 테스트셋에서 비교 가능한 prompt가 강하다.

#### 26. 3단계 — 실행 경로에는 timeout·error·fallback도 포함된다

- 정상선만 그린 architecture는 데모 문서다.
- 운영 문서에는 실패 branch와 책임 주체가 있어야 한다.

#### 27. 4단계 — 평균값보다 실패 분포와 사례를 함께 본다

- p50만 보면 tail latency를 놓친다.
- 평균 점수만 보면 특정 사용자·문서군의 반복 실패를 놓친다.

#### 28. 5단계 — 변경 이유와 결과가 함께 남아야 개선이다

- `v1 → 가설 → 실험 → 판정 → v2 또는 rollback`
- “더 좋아 보임” 대신 측정 축·대표 실패·trade-off를 남긴다.

#### 29. 한 요청의 최소 trace가 팀의 공통 언어다

- `trace_id / timestamp / task / prompt_version / provider / model`
- `status / latency / token / content fingerprint / error type`
- 기본 실습은 원문을 로그에 저장하지 않는다.

#### 30. 16주는 같은 순환을 점점 깊게 구현한다

- 01주: 최소 trace
- 02–03주: prompt와 evaluation
- 04–07주: context와 model adaptation
- 09–10주: serving와 observability
- 11–14주: evaluation·agent·safety·cost
- 15–16주: 하나의 운영 가능한 capstone

### D. TRACE/01 Lab — 31–38

#### 31. Definition of Done은 ‘세 번 호출’이 아니라 ‘한 개 비교표’다

- 실행 가능한 health endpoint
- 같은 input으로 trace 2건 이상
- 한 번에 변수 하나 변경
- 결과와 운영 지표를 함께 비교
- 다음 version 가설 2문장

#### 32. 설치보다 먼저 환경·서비스·모델 경로를 검증한다

```bash
uv python install 3.11.14
uv venv --python 3.11.14 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --app-dir week01/lab --reload
curl http://127.0.0.1:8000/health
```

- 기본 demo provider는 model download 없이 동작한다.
- Ollama 경로는 `ollama serve`와 설치 model tag를 별도로 확인한다.

#### 33. API 응답에는 생성 텍스트보다 많은 운영 데이터가 있다

- UI의 response와 trace를 함께 읽는다.
- `/docs`에서 request/response schema를 확인한다.
- `/api/v1/traces`, `/api/v1/stats`, `/metrics`의 관점 차이를 비교한다.

#### 34. Baseline을 고정해야 개선을 말할 수 있다

| 고정 | 변경 | 관측 |
|---|---|---|
| input, task, provider/model | prompt version 또는 temperature 하나 | output, status, latency, token, 판단 |

- 첫 실행을 버리지 않는다. baseline이 없으면 변화만 있고 개선은 없다.

#### 35. 요약은 길이·충실성·지연을 함께 본다

- task=`summarize`
- pass: 핵심 주장 유지, 사실 추가 없음, 요구 형식 준수
- 운영: latency와 token estimate 확인

#### 36. 정보 추출은 출력 schema가 평가 기준을 만든다

- task=`extract`
- `SIGNAL / FRICTION / NEXT ACTION`이 모두 있는지 확인
- 같은 입력을 Ollama로 실행할 때 형식 준수·내용·latency 비교

#### 37. Sampling 실험은 한 번에 변수 하나만 바꾼다

- demo provider는 결정론적 baseline이라 temperature가 출력을 바꾸지 않는다.
- Ollama provider에서 `0.2 → 0.8`만 바꾸고 나머지를 고정한다.
- 다양성이 늘었는지, 형식 준수나 사실성이 떨어졌는지 기록한다.

#### 38. 실행→비교→개선 기록이 다음 주 PromptOps의 입력이다

- exit ticket 1: 오늘 trace가 없었다면 무엇을 비교하지 못했는가?
- exit ticket 2: 다음 prompt version에서 무엇 하나를 바꾸고 어떤 지표로 판정할 것인가?
- 다음 주: prompt를 문장이 아니라 versioned product asset으로 다룬다.

## 현업 관점의 교수자 노트

- 학생이 설치에서 막히면 pair programming 또는 demo provider로 즉시 전환한다. 환경 복구 자체가 수업의 유일한 성과가 되지 않게 한다.
- “최신·가장 큰 모델”보다 같은 input과 평가 기준을 고정하는 습관을 먼저 만든다.
- 평균 latency 하나만 제시하면 p95의 의미를 묻고, 결과만 제시하면 prompt/model version을 묻는다.
- 실제 고객 원문을 복사하지 않게 한다. 실습 UI와 JSONL trace는 원문 대신 fingerprint만 남긴다.
- token 수치는 추정치임을 반복한다. Ollama 실측 metadata 또는 provider usage가 있을 때 그것을 canonical 값으로 사용한다.
- 실습 결과가 좋았다는 주장에는 항상 대표 실패 1개와 다음 개선 1개를 함께 요구한다.

## 근거

- [AS-IS 핵심 커리큘럼](../../AS-IS%202025%202nd%20semester/00_AS-IS_핵심_커리큘럼.md)
- [AS-IS 1주차 통합 강의안](../../AS-IS%202025%202nd%20semester/01_AS-IS_주차별_통합_강의안.md#01주차--orientation-및-llm-lifecycle)
- [AS-IS 1주차 디자인 콘티](../../AS-IS%202025%202nd%20semester/02_AS-IS_주차별_강의_디자인_콘티.md#01주차-콘티--orientation-및-llm-lifecycle)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)
- [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)
- [LoRA](https://arxiv.org/abs/2106.09685)
- [Ollama Chat API](https://docs.ollama.com/api/chat)
- [Ollama List models API](https://docs.ollama.com/api/tags)
