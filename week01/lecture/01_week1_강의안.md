# Week 01 — 호출 너머의 LLM 운영

## 강의 정의

- 핵심 문장: 수강생은 “LLM을 한 번 호출하는 사람”이 아니라 응답을 기록·평가·재현·개선하는 운영자로 첫 주를 마친다.
- 기본 운영: 180분 워크숍(개념·대화 110분 + 준비 20분 + 실습·회고 50분)
- 압축 운영: AS-IS 수업 단위에 맞춘 100분 핵심 경로
- 실습 서비스: `TRACE/01`, 필수 `demo` provider / 선택 `Ollama` provider
- 완료 조건: 실행 가능한 서비스, 같은 입력의 trace 2건 이상, 단일 변수 비교, 다음 개선 판단 2문장

## 이 과목의 라이프사이클 기준

이 강의에서 사용하는 5단계는 업계의 유일한 표준이나 모든 모델의 보편적 수명주기를 뜻하지 않는다. 2025년 2학기 실제 1주차 자료의 5단계 구조를 16주 산출물과 운영 증거에 맞춰 재정리한 **LLM 서비스 개선용 교육 프레임**이다.

1. 기획·데이터
2. 프롬프트·컨텍스트
3. 실행·배포
4. 평가·관찰
5. 개선·버전

`TRAINING / EVALUATION / DEPLOYMENT / MAINTENANCE / RETIREMENT`도 모델 또는 전체 AI 시스템의 생성부터 종료까지를 설명하는 가능한 분류다. 이 과목의 프레임과 경쟁하는 오답이 아니라 관리 대상과 목적이 다른 분류다. 특히 fine-tuning은 이 과목에서 여러 개선 레버 중 하나이며, retirement는 5단계 뒤에 자동으로 도달하는 종착점이 아니라 계속·교체·종료를 별도로 판단하는 운영 경계다.

이 과목은 다음 조건 때문에 서비스 개선 폐루프를 공통 좌표계로 채택한다.

- 기준: 성공 조건과 금지 조건
- 맥락: 사용자, 업무, 데이터, 권한
- 버전: 변경 대상과 변경 이유
- 평가: 같은 입력과 같은 판단 축의 비교

## 학습성과

수업을 마친 수강생은 다음을 수행할 수 있다.

1. AI → 딥러닝 → Transformer → LLM의 전환을 병목 이동의 관점으로 설명한다.
2. 모델 능력과 서비스 신뢰성의 차이를 사용자·맥락·성공·경계 계약으로 설명한다.
3. Prompt, Retrieval, Tool, Model Routing, SFT, RLHF/DPO, LoRA의 개입면과 비용·가역성을 구분한다.
4. DevOps, MLOps, LLMOps에서 운영 관심사와 관리 자산이 어떻게 누적되는지 설명한다.
5. 품질·지연·비용·안전·재현성을 이 과목의 공통 판단 축으로 사용한다.
6. 서비스 개선 폐루프를 자신의 사례와 16주 산출물에 매핑한다.
7. Python 3.11.14 환경에서 API를 실행하고 최소 trace schema를 확인한다.
8. 한 번에 변수 하나만 바꾼 baseline·variant 비교로 다음 version 가설을 제시한다.

## 강사 소개 — 공개용 기준

> 차성재 | AI Product Manager · 서울시립대학교/아주대학교 AI 부문 겸임교수  
> 금융(AutoML·MLOps) → 의료(Computer Vision·DataOps) → 교육(LLMOps·AICC) → 커머스(Agentic AI)의 제품 개발·운영 경험  
> 대학원 정규 강의와 기업 대상 Prompt Engineering·LLM/RAG/LLMOps·AI Native 실습형 교육  
> AI를 데모가 아닌 문제정의·PRD·프로토타입·평가·워크플로우·운영 지표로 연결  
> 《딥러닝의 정석 2판》 역자 · Microsoft Certified: Azure AI Engineer Associate

공개 저장소에서는 현직 회사명·팀명·내부 프로젝트·내부 지표·개인 연락처를 노출하지 않는다. 현직은 `대형 패션·라이프스타일 커머스 플랫폼의 AI Product Manager`로만 표현한다.

## 180분 운영표

| 시간 | 슬라이드 | 운영 | 현장 증거 |
|---:|---:|---|---|
| 00–12분 | 1–8 | 범위가 다른 두 라이프사이클, 과목 기준, 1주차 완료 계약 | 호출과 운영의 차이 한 문장 |
| 12–25분 | 9–16 | 강사 관점, 16주 누적 구조, 평가 원칙, 기준 사례 | 개인 관심 서비스와 대표 입력 1개 |
| 25–50분 | 17–31 | AI의 병목 이동, Attention, Transformer, Pretraining, 신뢰성의 공백 | 모델이 보장하지 않는 조건 2개 |
| 50–65분 | 32–44 | Prompt·RAG·Tool·Routing·SFT·선호 학습·LoRA | 사례에 먼저 적용할 레버와 이유 |
| 65–75분 | — | 휴식·2인 토의 | 가장 위험한 실패 가설 1개 |
| 75–100분 | 45–56 | Ops 관심사 확장, trace, 다섯 판단 축과 trade-off | 관리해야 할 실행 자산 5개 |
| 100–120분 | 57–64 | 서비스 개선 폐루프, 단계별 계약, 16주 정렬 | 개인 사례의 5단계 산출물 |
| 120–130분 | 65–70 | 실습 계약, 공통 환경, demo/Ollama 분기, preflight | `/health` 정상 응답 |
| 130–140분 | — | 휴식·Ollama warm-up | 실패자는 demo 경로 유지 |
| 140–172분 | 71–78 | API 계약, endpoint, UI, trace, 단일 변수 실험, 실패 복구 | 비교 가능한 trace 2건과 비교표 |
| 172–180분 | 79 | 개선 판단 공유와 PromptOps 연결 | 변경·기대·판정 2문장 |

## 100분 압축 운영표

| 시간 | 슬라이드 | 운영 |
|---:|---:|---|
| 00–10분 | 1–8 | 두 라이프사이클의 범위와 과목의 서비스 개선 기준 |
| 10–18분 | 9, 11–16 | 강사 관점, 과정 산출물, 평가, 고객 피드백 사례 |
| 18–32분 | 17–18, 21, 24, 26–31 | Transformer·Pretraining·모델 능력과 서비스 신뢰성 |
| 32–45분 | 32–34, 37–44 | 개입 비용·가역성, Prompt·Routing·Post-training |
| 45–62분 | 45–51, 56–64 | 운영 자산, 공통 판단 축, 폐루프와 단계별 계약 |
| 62–72분 | 65–70 | `TRACE/01` 계약, 환경 구성, provider 분기, health |
| 72–94분 | 71–78 | 타입 계약, endpoint, trace, A/B 실험, 실패 복구 |
| 94–100분 | 79 | 비교 판단과 다음 prompt version |

압축 경로에서는 역사적 사례·수식·개별 지표 설명을 줄이고, `과목 기준 → 신뢰성의 공백 → 개입 레버 → 운영 폐루프 → trace 실습`의 인과관계를 유지한다.

## 79장 슬라이드 콘티

### A. 기준과 수업 계약 — 1–8

#### 1. 호출 너머의 LLM 운영

- 화면: 검정 바탕, 대형 제목, `W01 / ORIENTATION · LIFECYCLE · TRACE`.
- 핵심: 모델 이름 암기보다 한 번의 실행을 trace와 비교 가능한 개선으로 전환하는 첫 수업.

#### 2. 맥락 없는 질문

- 화면: 질문 `LLMOps의 5단계는?`와 `1 TRAINING / 2 EVALUATION / 3 DEPLOYMENT / 4 MAINTENANCE / 5 RETIREMENT`의 세로 번호 목록.
- 핵심: 대상·목적·근거가 없는 질문은 범위가 다른 분류를 하나의 정답처럼 비교하게 만드는 구조.
- 교수자 경계: 목록 자체를 사실 오류로 단정하지 않고 모델·시스템 관점의 가능한 taxonomy로 소개.

#### 3. 다섯 단계의 범위 혼선

- 화면: `MODEL / SYSTEM VIEW`와 `COURSE / SERVICE VIEW`의 2분할.
- 핵심: 전자는 생성부터 종료까지의 수명주기, 후자는 운영 중 반복 개선의 폐루프.
- 관리 대상: 모델 또는 전체 AI 시스템과 LLM 애플리케이션·실행 증거의 구분.

#### 4. 두 라이프사이클의 적용 범위

- 화면: 관리 단위, 주요 목적, 종료 관점, 학습 위치의 4행 비교표.
- 핵심: maintenance는 서비스 프레임의 실행·관찰·개선에 걸치며 retirement는 별도 운영 판정 경계.
- 교수자 경계: 두 분류의 일대일 대응이나 우열 관계를 강요하지 않는 설명.

#### 5. 이 과목의 기준: 서비스 개선 폐루프

- 화면: `기획·데이터 → 프롬프트·컨텍스트 → 실행·배포 → 평가·관찰 → 개선·버전`의 순환 구조와 `계속·교체·종료` 경계.
- 핵심: 이미 학습된 기반 모델을 포함한 서비스를 반복적으로 관찰·개선하기 위한 16주 공통 좌표계.
- 교수자 경계: 업계의 단일 표준이 아니라 AS-IS 강의와 16주 산출물을 연결한 교육용 운영 프레임.

#### 6. 판정 가능한 개선의 조건

- 화면: `기준 / 맥락 / 버전 / 평가`의 대형 단어와 짧은 정의.
- 핵심: 정답 암기가 아니라 다른 사람이 같은 조건에서 다시 판정할 수 있는 운영 계약.
- 이번 주 초점: 버전 정보를 포함한 trace.

#### 7. 1주차 완료 상태

- 화면: 실행 서비스, trace 두 건, 단일 변수, 비교표, 개선 가설의 5개 완료 증거.
- 핵심: 설치 여부가 아닌 재현·비교·판정 가능한 산출물 묶음이 완료 기준.
- 운영: Ollama 준비가 늦으면 demo provider로 먼저 완주.

#### 8. 첫 호출의 전환

- 화면: `CALL → TRACE → COMPARE → IMPROVE`의 단일 흐름.
- 핵심: trace가 생성 결과와 동일 평가축의 비교를 연결하고 다음 version의 근거를 제공.

### B. 강사·과정·기준 사례 — 9–16

#### 9. 강사의 네 도메인 운영 경험

- 화면: 공개 프로필 사진, AI Product Manager·겸임교수·역자 역할, 금융·의료·교육·커머스 경험.
- 핵심: 모델 개발 자체보다 문제 정의부터 운영 지표까지 연결해 온 제품 관점.
- 공개 경계: 회사·팀·내부 프로젝트·내부 지표·연락처 제외.

#### 10. 정형 데이터에서 생성형 AI까지

- 화면: `FINANCE → HEALTHCARE → EDUCATION → COMMERCE` 경력선과 AutoML/MLOps, CV/DataOps, LLMOps/AICC, Agentic AI.
- 핵심: 도메인은 달라도 데이터·기술·운영 단위가 지속적으로 확장된 과정.

#### 11. 도메인을 관통한 운영 질문

- 화면: 중앙 `정확한가? 다음은?`과 재현성·관찰성·통제·설명의 방사형 구조.
- 핵심: 정확도만으로 끝나지 않는 서비스 운영의 네 후속 질문.

#### 12. 16주 누적 산출물

- 화면: W01 trace baseline부터 W15–16 operable capstone까지 이어지는 roadmap.
- 핵심: 매주의 notebook·log·version이 하나의 서비스 계약으로 누적되는 과정.
- 강조 기준: 마지막 capstone이 아니라 현재 출발 자산인 W01 trace의 의미 중심.

#### 13. 커리큘럼의 여섯 능력 축

- 화면: `PROMPT / RAG / ADAPT / SERVE / EVAL / GOVERN`의 6개 역량 축.
- 핵심: 분리된 도구 목록이 아니라 동일한 서비스 개선 폐루프의 여섯 능력.
- 운영 관점: 안전·비용·권한은 마지막 주제가 아니라 모든 축의 횡단 조건.

#### 14. 재현·비교·설명 중심 평가

- 화면: README·환경, config·version, trace·result, 판단·다음 가설과 평가 질문의 연결표.
- 핵심: 다른 사람의 재실행, 변경점 식별, 동일 축 비교, 승격·보류·rollback의 설명.
- 학사 경계: 점수와 일정은 해당 학기 LMS를 단일 기준으로 사용.

#### 15. 기준 사례: 고객 피드백 도우미

- 화면: 합성 고객 피드백 입력, 요약·구조 추출·실무 문장 재작성, 운영 증거 목록.
- 핵심: 이론과 실습 전체에서 같은 사례를 유지해 개념 변화와 실행 증거에 집중.
- 개인정보: 실제 고객 원문이 아닌 합성 문장만 사용.

#### 16. 눈에 보이는 호출과 운영 체계

- 화면: 수면 위 `PROMPT → MODEL → ANSWER`, 수면 아래 dataset·version·evaluation·timeout·fallback·safety·cost·owner.
- 핵심: 화면의 생성 결과보다 배포 판단에 필요한 운영 증거의 구조.
- 표현 경계: 근거 없는 `5% / 95%` 수치 대신 구조적 차이만 사용.

### C. 능력의 형성과 신뢰성의 간극 — 17–31

#### 17. 능력의 형성과 신뢰성의 간극

- 화면: Part 1 구분과 `규칙 · 데이터 · 연산 · Attention · Pretraining`.
- 핵심: AI 연도 암기 대신 다음 병목과 새로 추가된 운영 문제의 연결.

#### 18. AI 역사의 네 번의 병목 이동

- 화면: `RULE → LEARN → SCALE → GENERATE → OPERATE` timeline.
- 핵심: 새 능력은 기존 운영 문제를 지우지 않고 새로운 관리 대상을 추가.

#### 19. 규칙 기반 시스템의 경계

- 화면: 명시적 IF/THEN 규칙의 통제 가능성과 예외 조합 폭증의 2분할.
- 핵심: 작은 안정 범위의 설명 가능성은 강점, 모호한 언어·영상·복합 예외는 한계.
- 교수자 경계: 규칙 기반 AI를 낡은 기술로 단순 폄하하지 않는 균형.

#### 20. 데이터 기반 학습의 전환

- 화면: 사람이 규칙을 쓰는 흐름과 데이터에서 패턴을 추정하는 흐름의 before/after.
- 핵심: 오류 수정의 대상이 규칙에서 데이터·목표·모델로 확장되며 새 운영 자산이 발생.

#### 21. 딥러닝의 세 조건

- 화면: DATA·GPU·MODEL의 삼각 구조.
- 핵심: 딥러닝의 도약은 다양한 학습 신호, 병렬 연산, 역전파·아키텍처의 결합.

#### 22. 표현 학습의 변화

- 화면: hand-crafted feature pipeline과 representation learning pipeline 비교.
- 핵심: 사람의 역할은 사라진 것이 아니라 특징 선택에서 데이터·목표·평가 설계로 이동.

#### 23. 시퀀스 모델의 순차 병목

- 화면: TOKEN 1부터 TOKEN N까지 순차 state 전달과 긴 경로.
- 핵심: recurrent 처리의 순차 계산 대기와 멀리 떨어진 정보의 긴 전달 경로.
- 교수자 경계: Transformer 이전 모델 전체를 하나의 단순 구조로 일반화하지 않는 설명.

#### 24. Self-Attention의 핵심 질문

- 화면: `고객 / 은 / 교환 / 절차 / 불편` token 관계와 현재 token의 참조 가중치.
- 핵심: 현재 위치를 해석하기 위해 다른 위치를 얼마나 참고할지 계산하는 구조.

#### 25. 토큰 관계의 가중치 지도

- 화면: token 간 설명용 attention heatmap.
- 핵심: 색의 강도는 관계 가중치의 직관이며 실제 모델 측정값이나 인과 설명이 아님.

#### 26. Transformer의 관계 계산 구조

- 화면: `TOKENS → Q·K·V → ATTENTION → FFN → CONTEXT`.
- 핵심: 학습 시 시퀀스 위치의 병렬화와 장거리 관계 처리.
- 기술 경계: decoder 추론은 token별 autoregressive 반복이라는 조건 병기.

#### 27. Pretraining의 다음 Token 목표

- 화면: 대규모 corpus→문맥→다음 token 확률→loss→weight update.
- 핵심: 대부분의 생성형 decoder-only LLM에서 범용 언어 능력을 형성하는 대표 causal language modeling 목표.
- 교수자 경계: 모든 기반 모델의 목적함수가 동일하다는 일반화 금지.

#### 28. 범용 언어 능력의 목록

- 화면: 생성·요약·변환·분류·코드의 대형 keyword 구성.
- 핵심: 하나의 모델이 여러 자연어 작업을 수행해도 각 작업에는 별도 입력 계약과 평가 기준이 필요.

#### 29. 서비스 보장의 공백

- 화면: 생성 가능한 능력과 사실성·최신성·권한·지연·비용·안전의 2분할.
- 핵심: 확률적 일반화 능력과 반복 가능한 서비스 신뢰성의 분리.

#### 30. 생성형 시스템의 변동성

- 화면: 동일 코드 주위의 MODEL·CONTEXT·SAMPLING·PROMPT 변인.
- 핵심: 코드가 같아도 실행 조합의 변화로 output과 운영 지표가 달라지는 구조.

#### 31. 제품 정의의 잔여 과제

- 화면: `MODEL CAPABILITY ≠ SERVICE RELIABILITY`와 USER·CONTEXT·SUCCESS·BOUNDARY.
- 핵심: 사용자, 상황, 성공 조건, 금지 행동의 소유자는 모델이 아니라 제품·운영 팀.

### D. 서비스 행동의 개입 레버 — 32–44

#### 32. 서비스 행동의 개입 레버

- 화면: Part 2 구분과 `Prompt · Retrieval · Tool · Routing · Post-training`.
- 핵심: 모델을 변경하기 전에 개입 위치와 비용·가역성의 구분.

#### 33. 개입 레버의 비용·가역성 지도

- 화면: Prompt에서 fine-tuning으로 이어지는 비용·시간·rollback 용이성의 교육용 지도.
- 핵심: 이번 가설을 가장 싸고 빠르게 검증할 수 있는 첫 변경점의 탐색.
- 교수자 경계: 절대 기술 순위가 아니며 규제·지연·온디바이스·라이선스 제약은 순서를 변경.

#### 34. Prompt의 통제 범위

- 화면: ROLE·INSTRUCTION·EXAMPLE·OUTPUT SCHEMA의 계층.
- 핵심: model weight 바깥에서 빠르게 변경·version·rollback 가능한 행동 제어면.
- 다음 주 연결: 좋은 문장보다 template, version, schema, test set의 관리.

#### 35. Retrieval의 외부 근거

- 화면: `QUERY → SEARCH → EVIDENCE → CONTEXT → ANSWER`.
- 핵심: 최신·사내·출처 지식의 외부 context 공급.
- 교수자 경계: 검색 품질·근거 연결·권한을 별도 평가해야 하며 RAG를 모든 환각의 만능 해결책으로 설명하지 않음.

#### 36. Tool의 행동 경계

- 화면: 모델의 tool 이름·argument 제안과 runtime의 실제 API 실행 분리.
- 핵심: schema 검증·승인·권한·timeout·audit·idempotency는 runtime의 책임.

#### 37. Model Routing의 선택 축

- 화면: 짧은 분류, 근거형 답변, 복잡한 추론, 민감 데이터별 우선 축과 routing 기준.
- 핵심: 하나의 최고 모델이 아니라 품질·지연·비용·데이터 위치 제약에 맞는 선택.

#### 38. SFT의 행동 학습

- 화면: `TASK → EXAMPLES → LOSS → UPDATE → EVAL`.
- 핵심: 반복되는 형식·말투·도메인 행동을 좋은 입출력 예시로 적응.
- 교수자 경계: 명확한 반복 행동과 holdout 평가셋이 필요한 레버이며 지식 주입의 만능 도구가 아님.

#### 39. SFT 데이터의 최소 계약

- 화면: INSTRUCTION·INPUT·IDEAL OUTPUT의 triplet.
- 핵심: 실제 분포를 닮은 검수 입력, 고정 schema, 입력에 근거한 이상 출력.
- 데이터 경계: 민감 원문 제외와 학습·평가 데이터 분리.

#### 40. 선호 데이터의 구조

- 화면: 같은 prompt에 대한 CHOSEN과 REJECTED의 대비.
- 핵심: 선호 데이터의 최소 단위는 하나의 정답이 아니라 비교 pair와 명확한 rubric.

#### 41. 대표적인 PPO 기반 RLHF 경로

- 화면: `SFT → PREFERENCE → REWARD MODEL → PPO → EVAL`.
- 핵심: InstructGPT의 reward model과 PPO를 사용하는 대표 경로.
- 교수자 경계: RLHF 전체를 하나의 알고리즘과 동일시하지 않고 모든 구현의 세부 구조가 같다는 일반화 금지.

#### 42. DPO의 직접 선호 최적화

- 화면: PPO 기반 RLHF의 다단 경로와 DPO의 pair·reference·direct loss 경로 비교.
- 핵심: DPO는 별도 reward model과 on-policy RL 없이 preference pair와 reference policy로 직접 최적화.

#### 43. LoRA의 저랭크 변경 단위

- 화면: 고정 base weight와 학습 가능한 low-rank adapter.
- 핵심: 작은 artifact, 빠른 교체, base 공유, adapter 단위 실험이라는 PEFT 운영 이점.
- 교수자 경계: 고정된 메모리·비용 절감률을 주장하지 않고 설정 의존성 병기.

#### 44. 개입 순서의 기본 휴리스틱

- 화면: `BASELINE → PROMPT → RAG/TOOL → ROUTING → FINE-TUNING`.
- 핵심: 데이터·평가셋·배포 이득이 없으면 더 가볍고 되돌리기 쉬운 앞 단계에서 우선 검증.
- 예외: 규제·지연·온디바이스·라이선스 조건에 따른 순서 재배치.

### E. 운영 관심사와 판단 축 — 45–56

#### 45. 운영 관심사와 관리 자산의 확장

- 화면: Part 3 구분과 `Code · Data · Model · Prompt · Context · Trace · Evaluation`.
- 핵심: LLMOps는 MLOps의 대체가 아니라 기존 운영 관심사에 생성형 AI 자산을 추가하는 확장.

#### 46. DevOps·MLOps·LLMOps의 관심사 확장

- 화면: DevOps, MLOps, LLMOps의 누적 band.
- 핵심: code/build/release/runtime 위에 data/model/experiment, 다시 prompt/context/trace/evaluation이 추가되는 구조.

#### 47. LLM 서비스의 추가 운영 자산

- 화면: 중앙 trace id 주변의 prompt·context·response·evaluation.
- 핵심: version 가능한 prompt·config·dataset과 실제 실행 증거인 response·latency·status의 구분.

#### 48. 동일 코드의 서로 다른 동작

- 화면: 동일 commit·endpoint·schema와 서로 다른 prompt·context·model·config의 대비.
- 핵심: application code version만으로 생성 실행 전체를 재현할 수 없는 이유.

#### 49. 버전 조합의 실행 단위

- 화면: trace id, prompt version, provider/model, task/config, status/latency, content ref, output, token, timestamp.
- 핵심: trace id는 버전 자산과 실행 증거를 연결하는 join key.

#### 50. 이 과목의 다섯 공통 판단 축

- 화면: QUALITY·LATENCY·COST·SAFETY·REPRODUCIBILITY.
- 핵심: 업계의 고정 KPI 목록이 아니라 이 과목의 모든 실험에서 함께 확인할 공통 비교축.

#### 51. 판단 축 사이의 트레이드오프

- 화면: QUALITY↔COST, QUALITY↔LATENCY, SAFETY↔COVERAGE, CACHE↔FRESHNESS.
- 핵심: 한 축의 개선 주장에는 나머지 축의 regression 확인이 필요.

#### 52. 품질 지표의 업무 의존성

- 화면: 요약·정보 추출·RAG 답변·Agent 행동의 우선 품질축과 대표 실패 비교표.
- 핵심: 단일 범용 품질 점수 대신 task의 output contract와 실패 비용에 맞는 평가 기준.

#### 53. 지연시간의 분포 관점

- 화면: 평균, p50, p95/p99, timeout을 구분한 설명용 분포.
- 핵심: 평균만으로는 느린 꼬리 구간의 반복 사용자 경험을 설명할 수 없는 구조.
- 작은 표본: percentile과 함께 raw trace 확인.

#### 54. 요청 단위 비용의 구조

- 화면: `REQUEST COST = INPUT + OUTPUT + RETRIEVAL + TOOL + RETRY − CACHE`.
- 핵심: 모델 단가뿐 아니라 search·rerank·judge·tool·retry·fallback·cache를 포함한 전체 요청 경로.
- 교수자 경계: 정산 공식이 아닌 개념 구조이며 실제 단가는 당시 공급자 공식 문서 확인.

#### 55. 안전성의 권한·데이터 경계

- 화면: INPUT·RUNTIME·OUTPUT·STORAGE의 swimlane.
- 핵심: PII·injection·tool allowlist·human review·grounding·audit·retention·access control의 전 구간 적용.
- 운영 원칙: 안전을 마지막 검수 단계가 아닌 횡단 조건으로 취급.

#### 56. 재현성의 다섯 고정값

- 화면: 환경·입력·지시·실행·코드의 checklist.
- 핵심: Python/package/OS, dataset/fingerprint, prompt/schema, provider/model/config, commit/policy의 동시 고정.
- 교수자 경계: seed 하나만으로 생성 서비스 전체 재현성이 보장되지 않는다는 점.

### F. 서비스 개선 폐루프 — 57–64

#### 57. 서비스 개선 폐루프의 전체 구조

- 화면: 5단계 순환과 `계속·교체·종료` 경계, 전 단계를 가로지르는 다섯 판단 축.
- 핵심: 평가·관찰의 결과가 다음 기획과 변경 가설로 돌아가는 구조이며 특정 마지막 노드는 없음.
- 역할: 오프닝의 기준 정의를 운영 자산과 판단 축으로 확장한 통합 그림.

#### 58. 1단계 / 기획·데이터의 성공 계약

- 질문: 누구의 어떤 결정을 돕는가?
- 산출물: 대표 입력과 expected behavior, 성공·금지 조건과 평가셋, PII·license·retention 경계.
- 핵심: 성공 지표는 4단계에서 처음 생기는 것이 아니라 1단계에서 정의되고 4단계에서 측정.

#### 59. 2단계 / 프롬프트·컨텍스트의 버전 계약

- 질문: 무엇이 바뀌었고 왜 바뀌었는가?
- 산출물: prompt id/version/owner, input/output schema와 example, retrieval·tool context reference.
- 핵심: 읽기 좋은 prompt보다 고정 test set에서 비교 가능한 prompt.

#### 60. 3단계 / 실행·배포의 실패 경로

- 질문: 실패했을 때 어디로 흐르는가?
- 산출물: request/response contract, timeout·retry·fallback branch, health·release·owner.
- 핵심: 정상선만 있는 architecture는 운영 문서가 아니라 데모 문서.

#### 61. 4단계 / 평가·관찰의 분포 기준

- 질문: 누가, 언제, 어떻게 실패하는가?
- 산출물: quality와 대표 성공·실패, p50·p95·error rate, token·cost·safety signal.
- 핵심: offline evaluation과 production observation을 구분하면서 동일 version과 trace에 연결.

#### 62. 5단계 / 개선·버전의 판정 기록

- 질문: 다음 version은 무엇을 검증하는가?
- 산출물: v1→가설→단일 변경, 판정→v2 release 또는 rollback, trade-off와 다음 실패 가설.
- 핵심: 실패한 실험도 다음 선택지를 줄이면 유효하며 retirement는 자동 종착점이 아닌 별도 판정.

#### 63. 버전 변경의 최소 기록

- 화면: version, 가설, 변경, 판정의 changelog 예시.
- 핵심: version 번호 자체보다 `가설 → 변경 → trace → 판정`의 연결.
- 데이터 경계: 화면의 version과 결과는 형식 설명용 예시이며 실제 성능 수치가 아님.

#### 64. 16주와 다섯 단계의 정렬

- 화면: W01 contract, W02–05 prompt·RAG, W06–07 SFT·DPO, W09–10 API·trace, W11–14 eval·govern, W15–16 capstone.
- 핵심: Capstone 공통 계약은 API·log·KPI·version·재현 절차.
- 강조 기준: 마지막 capstone이 아니라 현재 Week 01의 성공 계약과 trace 기준선.

### G. TRACE/01 실습 — 65–78

#### 65. 첫 운영 루프의 실행

- 화면: Part 4 구분과 `Python 3.11.14 · FastAPI · Demo/Ollama · Trace · Compare`.
- 핵심: 설치 성공이 아니라 실행 서비스, trace, 비교표, 개선 가설까지 닫힌 운영 루프.

#### 66. TRACE/01의 서비스 계약

- 화면: Browser UI→FastAPI→Demo/Ollama provider와 trace store·관찰 endpoint의 architecture.
- 핵심: 한 요청에서 생성 결과와 운영 metadata를 함께 반환.

#### 67. 실습 완료의 다섯 증거

- 화면: health, trace 2건, 단일 변경, 비교 판단, 다음 가설.
- 핵심: 세 번 호출 자체보다 한 개의 비교표가 완료 기준.
- 운영: 설치 지연 시 demo provider로 필수 경로 우선 완주.

#### 68. 16주 개발환경의 공통 기준

- 화면: Python 3.11.14, course base, week profile, platform lock의 계층.
- 핵심: `>=3.11,<3.12`와 3.11.14 canonical patch, 공통 spine과 충돌 주차별 profile의 분리.

#### 69. 필수 경로와 선택 경로

- 화면: 동일 합성 입력에서 demo와 Ollama가 갈라진 뒤 같은 trace schema와 평가축으로 합류하는 흐름.
- 핵심: demo는 결정론적 필수 baseline, Ollama는 실제 생성 비교를 위한 선택 경로.

#### 70. 환경 구성과 Preflight 명령

- 화면: 다음 순서의 terminal 명령과 `{ "status": "ok" }` 성공 신호.

```bash
uv python install 3.11.14
uv venv --python 3.11.14 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --app-dir week01/lab
curl http://127.0.0.1:8000/health
```

- 핵심: 저장소 루트에서 Python→service→health를 순서대로 검증하고 실패 시 demo 경로 유지.

#### 71. 요청·응답의 타입 계약

- 화면: request의 task·provider·temperature, response의 output·trace, error의 status·detail 표.
- 핵심: UI보다 API schema가 서비스 계약의 기준이며 유효하지 않은 값은 validation에서 차단.

#### 72. 네 Endpoint의 관찰 범위

- 화면: `/api/v1/traces`, `/api/v1/stats`, `/metrics`, `/docs`의 역할 구분.
- 핵심: 개별 실행, 사람의 비교용 집계, 운영 수집 형식, request/response 계약 확인의 차이.

#### 73. 실제 화면의 관찰 지점

- 화면: `trace01-ui.png`와 입력/provider, 응답, trace metadata, 집계 지표의 4개 callout.
- 핵심: 생성 문장만 읽지 않고 실행 정체성과 운영 신호를 함께 읽는 순서.

#### 74. 한 요청의 최소 Trace Schema

- 화면: trace id, task, prompt version, provider/model, status/latency, token estimate, content fingerprint, UTC timestamp, error type.
- 핵심: 실행 비교에 필요한 최소 metadata와 원문 비저장 구조.
- 기술 경계: token estimate는 tokenizer 실측이 아닌 교육용 휴리스틱이며 모델 간 직접 비교 금지.

#### 75. Baseline·Variant의 단일 변수 실험

- 화면: 동일 입력·task·model을 고정하고 temperature `0.2 → 0.8`만 변경한 비교표.
- 핵심: output schema·사실성·latency를 동일 축으로 관찰.
- provider 경계: demo는 temperature를 의도적으로 무시하는 결정론적 baseline이며 sampling 차이는 Ollama 선택 경로에서 확인.

#### 76. 요약 태스크의 판정 기준

- 화면: FAITHFUL·COVERAGE·FORMAT·LATENCY의 네 ruler.
- 핵심: 자연스러운 문장뿐 아니라 새 사실 추가 여부, 핵심 보존, 요구 형식, 사용 맥락의 지연을 함께 평가.
- 데이터 경계: 화면 점수는 설명용 예시이며 실제 실습은 pass/fail rubric과 trace 값을 사용.

#### 77. 구조 추출의 판정 기준

- 화면: SIGNAL·FRICTION·NEXT ACTION의 세 필드와 grounded·specific·testable 조건.
- 핵심: 필드 존재 여부와 입력 근거성을 분리해 평가하고 누락·추가·검증 가능성을 우선 판정.

#### 78. 실패 유형별 복구 경로

- 화면: 422, 503, timeout, no delta와 각각의 복구 흐름.
- 핵심: 오류를 숨기지 않고 status·error type·복구 선택을 운영 증거로 기록.
- 수업 운영: Ollama 503이면 demo provider로 완주한 뒤 `ollama serve`와 model 설치를 별도 복구.

### H. 첫 주 운영 기록 — 79

#### 79. 첫 주 운영 기록

- 화면: CHANGE·EXPECT·JUDGE의 세 문장 골격과 `NEXT · PROMPT TEMPLATE · VERSION · EVALUATION · DEPLOYMENT`.
- exit ticket 1: 다음 prompt version에서 바꿀 한 가지.
- exit ticket 2: 예상 output 또는 운영 지표의 변화와 승격·보류·rollback 판정 기준.
- 다음 주 연결: 첫 trace와 개선 기록을 PromptOps의 첫 version 자산으로 전환.

## 현업 관점의 교수자 노트

- `TRAINING / EVALUATION / DEPLOYMENT / MAINTENANCE / RETIREMENT`를 틀린 답으로 처리하지 않는다. 먼저 관리 대상, 목적, 순환 여부, 종료 경계를 확인한다.
- 이 과목의 5단계가 업계의 단일 표준이라고 말하지 않는다. AS-IS 강의와 16주 산출물을 잇는 서비스 개선용 교육 프레임으로 범위를 고정한다.
- 학생이 설치에서 막히면 pair programming 또는 demo provider로 즉시 전환한다. 환경 복구가 수업의 유일한 성과가 되지 않게 한다.
- “최신·가장 큰 모델”보다 같은 input·version·평가 기준을 고정하는 습관을 먼저 만든다.
- 평균 latency 하나만 제시하면 p50·p95와 raw trace를 함께 묻고, 결과만 제시하면 prompt/model/config version을 묻는다.
- 실제 고객 원문을 복사하지 않게 한다. 실습 UI와 JSONL trace는 합성 입력의 fingerprint만 남긴다.
- `content_fingerprint`는 익명화가 아니라 동일 입력 확인용 축약 hash다. 추측 가능한 개인정보·기밀의 입력을 허용하지 않는다.
- token 수치는 교육용 추정치임을 반복한다. 실제 판단은 model tokenizer 또는 provider usage를 canonical 값으로 사용한다.
- 결과가 좋아졌다는 주장에는 대표 실패, 다른 판단 축의 regression, 다음 변경 가설을 함께 요구한다.
- 파랑 강조는 현재 초점·변경 변수·운영 증거처럼 맥락이 있을 때만 사용한다. 마지막 단계·마지막 장이라는 위치만으로 강조하지 않는다.

## 근거

- [AS-IS 핵심 커리큘럼](../../AS-IS%202025%202nd%20semester/00_AS-IS_핵심_커리큘럼.md)
- [AS-IS 1주차 통합 강의안](../../AS-IS%202025%202nd%20semester/01_AS-IS_주차별_통합_강의안.md#01주차--orientation-및-llm-lifecycle)
- [AS-IS 1주차 디자인 콘티](../../AS-IS%202025%202nd%20semester/02_AS-IS_주차별_강의_디자인_콘티.md#01주차-콘티--orientation-및-llm-lifecycle)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)
- [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)
- [LoRA](https://arxiv.org/abs/2106.09685)
- [AWS Generative AI Lens — lifecycle](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lifecycle.html)
- [Google Cloud — deploy and operate generative AI applications](https://docs.cloud.google.com/architecture/deploy-operate-generative-ai-applications)
- [Microsoft — foundation model lifecycle](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/manage-foundation-models-lifecycle)
- [NIST AI RMF — Secure and Resilient](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Python 3.11](https://docs.python.org/3.11/)
- [Ollama Chat API](https://docs.ollama.com/api/chat)
- [Ollama List models API](https://docs.ollama.com/api/tags)
