# AS-IS 2025년 2학기 LLMOps 주차별 강의 디자인 콘티

## 문서 역할

이 문서는 강의 “내용”뿐 아니라 어떤 순서와 화면 역할로 설명했는지를 복원한 storyboard다. 실제 PPTX/PDF의 1,002장을 기준으로 슬라이드 구간을 정리하고, Notion에 남은 초안·개정안 중 최종 통합에 적합한 흐름을 표시했다.

- 실제 화면 문구 검색: `03_AS-IS_슬라이드_텍스트_원문.md`
- 강의 운영·실습 상세: `01_AS-IS_주차별_통합_강의안.md`
- notebook 실행 정보: `practice/README.md`

## 전체 내러티브

```text
01–03  LLM·Prompt lifecycle과 평가/버전의 기준 수립
   ↓
04–05  외부 지식을 검색·재정렬하는 RAG 품질 개선
   ↓
06–07  모델을 SFT/LoRA/DPO로 도메인·선호에 정렬
   ↓
09–10  추론 API화 → 관찰·로그·버전·운영 체계화
   ↓
11–12  합성 평가데이터와 Agent workflow로 시스템 확장
   ↓
13–14  보안·안전·비용·스케일의 production constraint 적용
   ↓
15     공통 API/log/KPI contract를 갖춘 Capstone으로 통합
   ↓
16     팀별 결과 발표·보고서로 기말 평가
```

08주차는 중간고사, 16주차는 팀별 프로젝트 결과 발표로 실제 강의 일정표와 기존 실습 저장소 README에 기록되어 있다. 두 주차 모두 별도 강의 deck과 notebook은 없다.

## 공통 슬라이드 패턴

### 반복되는 기본 구조

1. 표지
2. 강의 내용/목차
3. 1부 agenda
4. 문제상황 또는 역사적 배경
5. 핵심 개념과 용어
6. 비교표·pipeline·architecture
7. 코드·실습 절차
8. 과제·rubric·제출물
9. Q&A/5분 휴식
10. 2부 실습 구분
11. 종료

실제 덱에서는 02·09·10·11·12·13·14주차의 `2부: 실습` 구분이 실습 설명 뒤에 놓여 있다. 통합 MD에서는 구분 슬라이드의 원래 위치를 따르지 않고 실습을 이론 직후로 재배치했다.

### 시각 체계

| 구간 | 기본 배경·색 | 반복 요소 | 주의점 |
|---|---|---|---|
| 01–10주차 | 흰 배경, 남색·보라 포인트 | 큰 section divider, icon/diagram, 비교표, code block | 긴 본문과 이미지가 많아 text density가 높음 |
| 11–15주차 | 어두운 남색, 라벤더·청색·시안 포인트 | 단계형 pipeline, 핵심개념 callout, code·checklist | 밝은 글자 대비와 코드 가독성 유지 필요 |

- 주 폰트: NanumGothic
- 혼용: 02주차 Inter/Consolas, 03주차 Noto Sans TC
- 전체 객체: 그림 약 1,894개, native table 43개, native chart 0개
- 이미지/도형으로 만든 표와 diagram이 많아 텍스트 추출본만으로 시각적 관계를 완전히 재현할 수 없다.

---

## 01주차 콘티 — Orientation 및 LLM Lifecycle

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Opening | 1–2 | 과목명과 전체 범위 제시 | 최소 표지 → 목차 |
| Instructor & contract | 3–15 | 강사 신뢰도, 수업 성격, 평가·운영 합의 | 경력 timeline, 역할·성과 bullet, 수업 안내 |
| AI history | 17–27 | 오늘의 LLM이 나온 배경 형성 | 연대기, 인물·사건 이미지, 전환점 headline |
| Deep learning shift | 28–40 | data/GPU/deep learning이 성능곡선을 바꾼 이유 | 단계 비교, architecture image, before/after |
| LLM & post-training | 41–51 | Pretraining 이후 SFT/RLHF/DPO/PEFT의 자리 | lifecycle band, 용어 카드 |
| Ops evolution | 52–60 | DevOps→MLOps→LLMOps로 운영 대상 확장 | 3단 비교표, 책임영역 map |
| LLM Lifecycle | 61–67 | 학기 전체를 묶는 개선순환 제시 | 5단계 cycle diagram, “지속적인 개선” 메시지 |
| Lab setup | 69–82 | 환경을 직접 구성하고 첫 호출 성공 | 6단계 checklist, command/code, Ollama 예제 |
| Close | 83–84 | Q&A와 다음 주 연결 | 단순 종료 화면 |

Notion 1주차 콘티는 표지·목차까지만 있으므로 실제 덱이 canonical storyboard다.

---

## 02주차 콘티 — PromptOps Basic

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Definition | 4–9 | Prompt Engineering을 운영 lifecycle로 확장 | 정의 비교, “왜 필요한가” 문제 카드 |
| Cost & limits | 10–25 | 실험 전 model/quota/cost constraint 인식 | 가격·한도 표, RPM/TPM diagram, context 비교 |
| PromptOps Cycle | 26–33 | 수업의 8단계 기준선 수립 | 단계별 full-screen divider와 요약 |
| Setup Layer | 34–46 | 기본 prompt control을 작은 실험으로 축적 | `설명 → 예시 prompt → output/code` 반복 |
| Reasoning Aids | 47–61 | 복잡한 문제를 분해·도구화 | Zero/Few-shot, CoT, ToT, ReAct, PAL 비교 |
| Orchestration | 62–74 | 여러 호출과 Tool을 workflow로 연결 | function schema, chain flow, meta/APE loop |
| Safety & Branching | 75–84 | 운영 실패에 대한 분기·복구 | sentiment branch, filter, retry/backoff, fallback |
| Close | 85–88 | 요약·Q&A·종료 | 실제 실습은 앞 구간의 code slide에 이미 포함 |

Notion의 9장 기준 콘티는 `문제 정의 → 모델·비용 → 템플릿 → 실험 → 평가 → 버전 → 배포 → 모니터링 → 전체 요약`이다. 실제 덱은 이를 88장으로 확장한 반복형 storyboard다.

---

## 03주차 콘티 — Prompt Evaluation & Version Management

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Opening | 1–7 | 평가·버전의 필요성과 학습성과 제시 | title, agenda, output checklist |
| Project catalog | 8–19 | 10개 유형의 서로 다른 평가문제 인식 | 유형별 동일 template: 목표/리스크/지표/test set |
| Metric system | 20–38 | 정확성·품질·안전·운영·코드 지표를 체계화 | metric definition, formula/example, rubric 표 |
| Version & SSOT | 39–49 | SemVer, label, Notion/GitHub/Langfuse 연결 | lifecycle, DB schema, Prompty/PR link map |
| Tool comparison | 50–58 | Trace/Prompt/Dataset/Evaluation 구분 | Langfuse vs LangSmith 비교표, UI capture |
| Lab | 60–62 | 회의록 v0.0.1→v0.0.2 A/B | transcript→trace→dataset→evaluation flow |
| Close | 63–64 | 산출물 재확인 | checklist, Q&A |

Notion의 31장 [상세 PPT 콘티](https://synonymous-faucet-52e.notion.site/26fa18c366b180ed8611e2d3495745d5)는 10개 사례(4–13), 지표(14–18), 버전/SSOT(19–24), Langfuse 개념·비교(25–31)의 명확한 골격을 제공한다.

---

## 04주차 콘티 — Basic RAG & VectorDB

### Notion 원본 조합

1. [1–2 내용](https://synonymous-faucet-52e.notion.site/1-2-276a18c366b1800e8ffadb6484b759b5): 25장 — 필요성·역사·7단계 pipeline
2. [3–4 내용](https://synonymous-faucet-52e.notion.site/3-4-276a18c366b1807c85c2c9e0cfe41bcf): 24장 — embedding·ANN·VectorDB·chunk/meta
3. [5–6 내용](https://synonymous-faucet-52e.notion.site/5-6-276a18c366b180fd91fce68515ecb338): 26장 — 한국어 dataset·사례·평가·리스크
4. [실습 준비](https://synonymous-faucet-52e.notion.site/276a18c366b1805e83c5ef810f9a8fe2): 40분 Quick Lab

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Why RAG | 4–11 | 최신성·근거·환각 문제를 검색으로 해결 | problem/solution 대비, history timeline |
| 7-stage pipeline | 12–25 | corpus에서 grounded answer까지 부품 분해 | 한 단계 한 장, pipeline 위치 highlight |
| Embedding/ANN/DB | 26–37 | semantic space→approximate search→운영 DB | vector diagram, HNSW/IVF/PQ 비교, DB map |
| Data design | 38–49 | model보다 먼저 chunk/meta 품질을 설계 | MTEB, content-type chunk, metadata checklist |
| Korean sources/cases | 50–62 | 한국어 실습·project의 현실적 data source 제시 | dataset card, 국내 사례, license/security |
| Evaluation/risk | 63–74 | retrieval/generation/operations를 계측 | metric table, risk register, dashboard |
| Quick Lab | 76–80 | KorQuAD→embedding→upsert→search→Recall@5 | timebox, code step, expected artifact |
| Close | 81–85 | 다음 주 hybrid/rerank 예고 | summary, Q&A |

Google/Perplexity/ChatGPT/Claude 페이지는 final storyboard가 아니라 research draft로 분리한다.

---

## 05주차 콘티 — Advanced RAG

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Scenario & baselines | 4–12 | 한국어 법률/금융 검색에서 dense와 BM25가 각각 실패 | query/result card, 실패 highlight, 비교표 |
| Part A Hybrid | 13–22 | 두 검색을 RRF/weighted로 결합 | pipeline, rank table, α slider concept |
| Part B Re-ranking | 23–30 | 상위 후보의 정밀도를 Cross-Encoder로 개선 | Top-N→score→Top-k funnel |
| Part C Korean design | 31–38 | 표/목록/조문/개정/권한을 pipeline에 반영 | document structure, metadata/field map |
| Part D Evaluation | 39–52 | 단계별 개선을 Recall/MRR/NDCG로 검증 | baseline/after chart, failure taxonomy, checklist |
| Lab | 54–58 | MIRACL-ko+BGE-M3+Pinecone/BM25+reranker | notebook sequence, function names, output table |
| Close | 59–61 | FAQ·Myth/Fact·다음 주 연결 | recap cards |

Notion에는 40장 초안과 [48장 개정안](https://synonymous-faucet-52e.notion.site/5-02-27da18c366b1806dbda1e71af1fa83c1)이 있다. 개정안의 `문제상황 → 두 baseline → fusion → rerank → 한국어 flow → 평가/운영`을 canonical narrative로 본다.

---

## 06주차 콘티 — SFT & LoRA

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| SFT context | 4–8 | lifecycle에서 SFT의 문제와 효과 정의 | stage map, before/after examples |
| Dataset & template | 9–17 | Instruction/Chat schema와 data quality 설계 | JSON/message example, masking/packing checklist |
| PEFT/LoRA/QLoRA | 18–23 | memory·cost를 줄이는 adapter 학습 | matrix/rank intuition, target module map, comparison |
| Infra/repro/eval | 24–30 | 재현 가능한 학습과 평가 기준 | tool stack, repo tree, cost/time, rubric |
| LoRA Lab | 32–41 | data→config→train→compare→artifact | sequential notebook steps, log/sample table |
| Wrong copied block | 42–45 | 05주차 RAG 실습의 잘못된 복제 | 본 주차 이야기에서 제외, 결함 표기 |
| Close | 46–48 | DPO 예고·Q&A | alignment bridge |

Notion의 32장 콘티는 `roadmap → lifecycle → SFT/data → LoRA/QLoRA → infra/repo → pipeline/eval → lab → error taxonomy → next DPO`로 구성된다.

---

## 07주차 콘티 — DPO

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Motivation | 4–8 | RLHF의 복잡성에서 DPO 필요성 도출 | alignment spectrum, RLHF vs DPO |
| Objective/data | 9–18 | preference pair와 β/reference policy 이해 | prompt/chosen/rejected cards, objective decomposition |
| TRL/evaluation | 19–30 | 구현 config와 bias·metric 통제 | mini code, config table, judge/human rubric |
| Lab | 32–39 | Week06 adapter→DPO→A/B→CSV | step checklist, Base/DPO comparison |
| Close | 40–42 | alignment 결과 회고 | summary/Q&A |

7주차는 Notion 상세 콘티가 없으므로 실제 덱과 notebook이 canonical source다.

---

## 08주차 콘티 — 중간고사

Notion에는 항목이 없고 별도 deck/notebook도 없지만, 01주차 실제 일정표와 [기존 실습 저장소 README](https://github.com/smilesjcha/ajou-llmops-2025-2nd-semester/blob/main/README.md)가 중간고사로 명시한다. 실제 평가표 기준은 대면 객관식 30문항, 성적 30%다. 시험 문항 원문은 없어 별도 콘티를 재구성하지 않는다.

---

## 09주차 콘티 — Inference Optimization & FastAPI

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Inference bottleneck | 6–17 | latency를 분해하고 quantization/cache lever 제시 | formula, Q4/Q5/Q8 table, cache layers |
| FastAPI/ASGI | 18–30 | model call을 typed async API로 전환 | request/response schema, async code, server comparison |
| GIL/concurrency | 31–39 | I/O/CPU/GPU workload에 맞는 병렬화 선택 | thread/process diagrams, timing examples |
| Production architecture | 40–47 | stateless API와 external state/queue 분리 | Nginx/ALB→API→worker→Redis/DB architecture |
| API tooling | 48–52 | contract와 client test를 표준화 | OpenAPI/Postman/Insomnia screenshots |
| SLI/SLO/load | 53–63 | 서비스 성능을 p95/throughput/error로 검증 | percentile graph, Locust/k6 flow, SLA table |
| Serving/ops | 64–78 | vLLM/TGI/Ollama, streaming, retry, auth, K8s | option matrix, SSE/WebSocket, HPA/PDB |
| Close | 79–82 | 과제·Q&A | s.80 lab divider는 실제 순서상 뒤늦음 |

Notion은 1–30p, 31–60p로 분할되어 있으며 실제 내용은 55장+부록이다. 실제 덱은 개념·운영 예시를 추가해 82장으로 확장했다.

---

## 10주차 콘티 — LLMOps Stack

### Notion 우선 버전

1. [1–20p 디자인 02](https://synonymous-faucet-52e.notion.site/1-20p-02-29fa18c366b180388a15f84012f16f28)
2. [21–40p ver02](https://synonymous-faucet-52e.notion.site/21-40p-ver02-29fa18c366b18061b392f91e058bfaf0)
3. [41–60p](https://synonymous-faucet-52e.notion.site/41-60p-29fa18c366b180f1b5e9d8ae781f7b27)
4. [61–80p](https://synonymous-faucet-52e.notion.site/61-80-29fa18c366b180f08191fda6bc10f7a6)

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Ops definition | 4–23 | 09주차 API를 “운영 가능한 상태”로 확장 | DevOps/MLOps/LLMOps evolution, lifecycle, metric map |
| Tool landscape | 24–39 | cloud/OSS/serving/pipeline 도구를 역할별 배치 | Azure/AWS/GCP mapping, OSS stack table |
| Core telemetry | 40–44 | latency/tokens/cost/error/quality log schema 확정 | field table, trace hierarchy |
| Lab & assignment | 45–60 | Langfuse/CSV/FastAPI hook으로 직접 기록 | option A/B/C, code/schema, analysis/rubric |
| Security/cost/SLA | 61–84 | 로그 시스템의 PII·retention·RBAC·budget·deployment 고려 | masked log examples, access table, SLA/dashboard |
| Capstone bridge | 85 | project proposal에 observability contract 포함 | research prompt/checklist |
| Close | 86–89 | summary/Q&A | s.87 lab divider는 뒤늦음 |

초기 1–20p 초안과 디자인 ver01은 대안 이력으로 보존하고 최종 통합에는 디자인 02를 사용한다.

---

## 11주차 콘티 — Synthetic Data & RAG Evaluation

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Need & types | 4–24 | data scarcity/privacy/long-tail 문제와 synthetic 전략 제시 | real vs synthetic, type cards, pipeline |
| Generation strategy | 25–35 | LLM/local/nlpaug 선택과 JSON/evidence control | prompt template, JSON example, risk checklist |
| Metrics | 36–46 | retrieval와 generation 평가를 분리 | Recall/MRR/NDCG formula/example, Faithfulness |
| Eval pipeline | 47–54 | documents→retriever→gold QA→loop→comparison | Step 1–5 full flow |
| Lab/report | 55–67 | TF-IDF baseline·augmentation·Recall graph·export | A–F lab checklist, notebook cells, submission tree |
| Close | 68–71 | rubric·Q&A | s.69 lab divider는 뒤늦음 |

Notion의 세 하위 페이지는 1–20, 21–40, 41–60에 해당하는 연속 원고로 사용한다.

---

## 12주차 콘티 — Agent Chaining

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Environment & Chain | 11–18 | 기본 Chat을 LCEL pipeline으로 묶음 | install/env, helper, `prompt | model | parser` code |
| Memory | 19–23 | stateless chat에 session history 추가 | state before/after, history store, code |
| Tool & Agent | 24–42 | 작은 Tool을 Agent가 선택·조합 | `@tool` cards, ReAct loop, stream messages |
| LangGraph | 43–56 | 선형 chain을 state graph·router로 확장 | State/Node/Edge, graph topology, transition code |
| Observability | 57–74 | 동일 callback으로 Chain/Agent/Graph 관찰 | Trace/Span hierarchy, metadata, UI capture |
| Close | 75–78 | 종합·Q&A | s.76 lab divider는 뒤늦음 |

Notion은 1–20, 21–40, 41–60만 존재하고 61–80 Langfuse 원고는 누락되어 있다. 실제 덱의 s.57–74가 이 공백을 채운다.

---

## 13주차 콘티 — Security & Safety

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Threat model | 4–12 | Security/Safety/Privacy와 공격면 정의 | taxonomy, attack cards, regulation map |
| Defense architecture | 13–25 | Safety Sandwich와 least privilege | layered architecture, control checklist |
| PII/API/RAG guard | 26–35 | code path에 input/output/retrieval control 삽입 | regex/code, middleware flow, safety label |
| Red Team & SLI | 36–45 | 공격성공률·오탐·latency를 측정 | test matrix, ASR formula, dashboard |
| Lab/assignment | 46–55 | 방어 2종 이상을 구현·로그 | step-by-step code, CSV schema, rubric |
| Governance | 56–63 | incident/retention/RBAC/RACI/DPIA로 운영 확장 | process diagram, responsibility table |
| Close | 64–67 | recap/Q&A | s.65 lab divider는 뒤늦음 |

Notion 13주차는 빈 페이지이므로 실제 덱과 notebook이 canonical source다.

---

## 14주차 콘티 — Cost Optimization & Auto Scaling

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Cost model | 4–15 | request와 월간 비용·latency·throughput 계산 | formula, worked example, distribution |
| Optimization & scaling | 16–23 | cache/batch/scale-up/out/HPA/KEDA lever | before/after, architecture, option table |
| SLI/SLO & logs | 24–30 | 비용과 품질·latency를 함께 관찰 | telemetry schema, SLO budget |
| Routing/operations | 31–53 | compression, small→large escalation, queue/DLQ, alert | routing tree, queue flow, dashboard |
| Cost lab | 54–63 | CSV→tokens→cost→scenario→visualization | step checklist, pandas graph, output files |
| Close | 64–67 | report·Q&A | s.65 lab divider는 뒤늦음 |

Notion 14주차는 빈 페이지이므로 실제 덱과 notebook이 canonical source다. 출처·가정이 없는 절감률은 illustrative example로만 표시한다.

---

## 15주차 콘티 — Capstone Project

| 구간 | 실제 슬라이드 | 내러티브 역할 | 화면·카피 패턴 |
|---|---:|---|---|
| Workshop contract | 5–9 | 목표·역할·milestone·risk 합의 | roadmap, role cards, checklist |
| Common repo/data/log/KPI | 10–23 | 모든 팀에 동일한 system contract 부여 | repo tree, log schema, Q/L/T/C/S table |
| API/implementation standard | 24–44 | reusable endpoints, adapter, cache/queue, config/CI | architecture, endpoint table, code/config examples |
| Seven team patterns | 45–64 | domain별 문제·가설·지표·wireframe 제시 | 팀마다 동일 card: problem/data/method/KPI/risk |
| Finish/package/rubric | 65–74 | 실험을 재현 가능한 제출물로 수렴 | milestone, artifact tree, rubric matrix |
| Close | 75–76 | 발표·Q&A | minimal close |

s.3은 14주차 agenda의 복제 오류이고 s.4는 이미지 전용이다. Notion에는 별도 15주차 페이지가 없다.

---

## 16주차 콘티 — 기말고사·팀별 프로젝트 결과 발표

별도 Notion 주차 페이지, deck, notebook은 없다. 01주차 실제 일정표와 기존 실습 저장소 README는 Week16을 `기말고사 — 팀별 프로젝트 결과 발표`로 명시한다. 실제 평가표는 프로젝트 보고서와 발표를 합쳐 성적 30%로 안내한다.

발표 흐름은 15주차 Capstone contract에 따라 다음 증거를 점검한다.

1. 문제·사용자·가설
2. baseline과 개선안
3. 고정 evaluation set
4. 품질(Q)·지연(L)·처리량(T)·비용(C)·안전(S)
5. 대표 성공·실패 사례
6. 실행 명령·환경·commit·config
7. 한계와 다음 개선안

---

## AS-IS 결함·편집 우선순위

| 우선순위 | 위치 | 결함 | 통합 MD 처리 |
|---|---|---|---|
| 높음 | 06주차 s.42–45 | 05주차 RAG 실습 4장 완전 복제 | SFT 본문에서 제외하고 결함으로 기록 |
| 높음 | 15주차 s.3 | 14주차 agenda 완전 복제 | Capstone agenda로 사용하지 않음 |
| 낮음 | 08·16주차 | 시험 주차라 별도 deck/notebook 없음 | 일정·평가 근거만 기록하고 시험 내용을 임의 생성하지 않음 |
| 중간 | 04주차 s.3 | 03주차 장 제목 잔존 | 올바른 RAG 제목으로 index하되 원문 결함 표기 |
| 중간 | 09주차 s.37 | 빈 슬라이드 | 검색 원문에는 빈 장으로 보존, 운영본에서는 건너뜀 |
| 중간 | 10주차 s.3 | 09주차 장 제목 잔존 | 올바른 LLMOps 제목으로 index하되 결함 표기 |
| 중간 | 12주차 s.3 | 11주차 agenda 문구 잔존 | Langfuse observability로 실제 흐름 보완 |
| 중간 | 13주차 s.6 | 제목 `스트·템플릿`으로 잘림 | 위협/테스트 문맥으로만 설명, 원문 임의 복원 금지 |
| 낮음 | 다수 후반 주차 | `2부: 실습`이 실습 뒤에 위치 | 운영 MD에서 theory 직후로 재배치 |
| 낮음 | 02주차 | 2025년 가격·quota 자료 | 역사적 기준일 표시 |

## 향후 개편 시 유지할 강의 디자인 규칙

1. 한 슬라이드는 하나의 질문에 답한다.
2. `왜 필요한가 → 어떻게 작동하는가 → 어떻게 측정하는가 → 무엇을 제출하는가`를 매주 유지한다.
3. 비교표는 같은 dimension과 단위를 사용한다.
4. 코드 앞에는 input/output contract, 코드 뒤에는 expected artifact를 둔다.
5. 실습의 metric 이름을 이론의 metric 이름과 동일하게 유지한다.
6. 유료 API와 무료/local fallback을 같은 단계에서 나란히 제시한다.
7. 가격·모델·라이브러리 API처럼 변하는 정보는 기준일을 표시한다.
8. PII·API key·외부 side effect를 실습 시작 전에 경고한다.
9. 오류·실패 사례를 삭제하지 말고 원인·복구·재현 조건과 함께 남긴다.
10. Capstone은 앞 주차의 prompt, retriever, adapter, API, log, evaluation, safety, cost artifact를 재사용한다.
