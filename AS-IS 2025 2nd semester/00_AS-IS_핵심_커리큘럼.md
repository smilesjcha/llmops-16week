# AS-IS 2025년 2학기 LLMOps 핵심 커리큘럼

## 문서 목적

이 문서는 2025년 2학기 `AI융합실전프로젝트10(LLMOps)`의 기존 커리큘럼을 한눈에 확인하기 위한 기준 문서다. 공개 Notion의 주차별 커리큘럼, 주차별 하위 콘티, 실제 PPTX/PDF 14개, 기존 실습 저장소의 notebook 16개를 함께 대조했다.

- 기준 학기: 2025년 2학기
- 수업 단위: 주차당 100분(이론 60분 + 실습 40분)
- 전체 설계: 16주차(08주차 중간고사, 16주차 팀별 프로젝트 결과 발표)
- 실제 강의자료: 01–07주차, 09–15주차의 PPTX/PDF 14쌍, 총 1,002장
- 실습자료: 01–07주차, 09–14주차 notebook 16개
- 08주차: Notion 요약에는 빠졌고 별도 PPTX/PDF·notebook은 없지만, 실제 강의자료 일정표와 기존 실습 저장소 README가 모두 `중간고사`로 명시한다.
- 16주차: 별도 PPTX/PDF·notebook은 없지만 동일한 두 일정 근거가 `기말고사 — 팀별 프로젝트 결과 발표`로 명시한다.

## 원자료 우선순위

내용이 서로 다를 때는 다음 순서로 AS-IS를 판정한다.

1. 실제 배포된 PPTX/PDF의 화면 내용
2. 주차별 Notion 하위 페이지의 강의안·디자인 콘티
3. Notion의 주차별 커리큘럼 요약
4. 기존 실습 저장소의 notebook과 지원 파일

PPTX와 PDF는 모든 주차에서 슬라이드/페이지 수가 일치한다. 다만 도형·그룹·이미지의 검색 가능성 차이 때문에 텍스트 추출 결과는 일부 다르며, 가격표·agenda·그래픽 설명은 PDF가 더 잘 잡히는 경우가 있다.

## 교육 방향

### 1. 전체 라이프사이클을 하나의 개선 루프로 다룬다

`기획·데이터 → PromptOps/RAG/Fine-tuning → Serving → Evaluation/Observability → Security/Cost → 개선·버전관리`를 연결한다. 한 번 모델을 만드는 수업이 아니라, 품질·지연·비용·안전 지표를 관찰하며 지속적으로 개선하는 운영 수업이다.

### 2. 유료 산업 스택과 무료 실습 경로를 병기한다

- 유료·관리형: OpenAI/Azure OpenAI, Claude, Gemini, Pinecone, Langfuse Cloud, W&B, Runpod 등
- 무료·로컬: Hugging Face, Ollama/llama.cpp, FAISS/Qdrant Local, CSV logging, pandas/Streamlit 등
- 원칙: 산업에서 쓰는 개념과 도구 지형은 폭넓게 배우되, 기본 실습과 과제는 로컬·무료 경로로도 완주할 수 있게 한다.

### 3. 매주 재사용 가능한 산출물을 남긴다

- Prompt template와 버전 로그
- 검색·평가 notebook
- LoRA/DPO adapter와 비교 리포트
- FastAPI 서비스와 부하테스트 결과
- 공통 LLMOps 로그와 dashboard
- 보안·비용·평가 리포트
- Capstone repository와 발표 자료

## 핵심 학습성과

수강생은 수업을 마친 뒤 다음을 수행할 수 있어야 한다.

1. LLM 서비스의 라이프사이클과 LLMOps 구성요소를 설명한다.
2. 프롬프트를 템플릿화하고 버전·평가·배포 라벨·실행 trace를 관리한다.
3. 한국어 문서를 위한 기본/고급 RAG를 설계하고 Recall/MRR/NDCG 등으로 평가한다.
4. SFT·LoRA·QLoRA·DPO의 역할과 적용 조건을 비교하고 소형 모델 실습을 수행한다.
5. FastAPI 기반 추론 API를 구성하고 quantization, cache, async, load test를 적용한다.
6. latency, tokens, cost, error, quality, safety를 공통 스키마로 로깅하고 분석한다.
7. Chain, Tool, Agent, Memory, LangGraph workflow를 구성하고 실행을 관찰한다.
8. Prompt injection, jailbreak, PII, retrieval poisoning에 대한 다층 방어를 설계한다.
9. 토큰 비용·처리량·지연을 추정하고 caching/routing/autoscaling 시나리오를 비교한다.
10. 품질·운영·안전 지표가 포함된 재현 가능한 Capstone을 설계·제출한다.

## 주차별 핵심 커리큘럼

| 주차 | 핵심 주제 | 이론 핵심 | 기본 실습·산출물 | 평가·과제 |
|---:|---|---|---|---|
| 01 | Orientation & LLM Lifecycle | AI/LLM 역사, Transformer, SFT·RLHF·DPO·PEFT, DevOps–MLOps–LLMOps, 5단계 lifecycle | Python 3.11 환경, GitHub 구조, Ollama 설치, 요약·Q&A·스타일 변환 | 환경 점검, 실행 로그, 자기소개/팀 구성 |
| 02 | PromptOps Basic | 문제정의, 모델·비용·한도, prompt template, reasoning, orchestration, safety/branching | OpenAI/Ollama 비교, Zero/Few-shot, CoT, ToT, ReAct, PAL, Tool Call, retry/fallback | 동일 task의 Prompt Variation 3종 비교 리포트 |
| 03 | Prompt Evaluation & Version Management | 프로젝트 유형별 평가축, offline/online metric, SemVer, 배포 라벨, SSOT, Langfuse/LangSmith | 회의록 prompt v0.0.1→v0.0.2, Trace, Dataset/Evaluation, Prompty | 개선 로그, PR, prompt 배포, 평가 리포트 |
| 04 | Basic RAG & VectorDB | RAG 7단계, chunk/metadata, embedding, ANN, HNSW/IVF/PQ, VectorDB, 한국어 데이터 | KorQuAD 2.0 → MiniLM → Pinecone/로컬 대안 → Top-k → Recall@5 | PDF/문서 기반 QA notebook |
| 05 | Advanced RAG | Dense+BM25, RRF/weighted fusion, metadata filter, Cross-Encoder rerank, 한국어 구조 | MIRACL-ko, BGE-M3, Pinecone/BM25, RRF/weighted, BGE reranker, Ollama | baseline 대비 Recall/MRR/NDCG 개선 비교 |
| 06 | Fine-tuning I: SFT & LoRA | Instruction/Chat schema, masking/packing, PEFT, LoRA rank/alpha/target, QLoRA | TinyLlama, train/val JSONL, LoRA adapter, Base-vs-LoRA CSV | 작은 데이터셋 Before/After notebook·리포트 |
| 07 | Fine-tuning II: DPO | RLHF 한계, preference pair, DPO objective, β/reference policy, length bias | Week06 adapter, DPOTrainer, β A/B, Base-vs-DPO 비교 | preference 품질·안전·스타일 평가 |
| 08 | 중간고사 | 01–07주차 이론·실습 점검 | 별도 실습 없음 | 대면 객관식 30문항, 성적 30% |
| 09 | Inference Optimization & FastAPI | Q4/Q5/Q8, GGUF, KV/response cache, FastAPI/ASGI/async, GIL, SLI/SLO/SLA, load test | Mini Chatbot API, SSE/cache/rate limit, Locust/k6 | README·코드·부하테스트 결과 |
| 10 | LLMOps Stack | MLOps vs LLMOps, Azure/AWS/GCP, MLflow/Langfuse/W&B, observability, 공통 log schema | Langfuse Trace 또는 CSV fallback, FastAPI logging hook, pandas 분석 | 09–10주차 통합 API+로그 과제 |
| 11 | Synthetic Data & RAG Evaluation | 문서→Q&A, paraphrase, hard negative, Recall/Precision/MRR/NDCG/Faithfulness | TF-IDF retriever, QA 10개+, nlpaug 선택, Recall@1/3/5, 시각화 | documents/QA/notebook/report 패키지 |
| 12 | Agent Chaining | LCEL, Memory, Tool, Agent, ReAct, StateGraph, Langfuse observability | calculator/time/summary tool, Agent+Memory, LangGraph router | Tool 2개 이상을 연결한 workflow notebook |
| 13 | Security & Safety | threat model, prompt injection/jailbreak, PII, moderation, RAG label, red team, governance | 한국어 PII masking, Detoxify 선택, FastAPI guard, audit log | 방어 2종 이상 + CSV 지표 리포트 |
| 14 | Cost Optimization & Auto Scaling | 비용식, cache/batch/routing, HPA/KEDA, queue/DLQ, SLO와 예산 | tiktoken, per-request/monthly cost, cache what-if, autoscale simulation | 비용 CSV·시각화·시나리오 리포트 |
| 15 | Capstone Project | 공통 API/log/KPI contract, 7개 팀 주제, milestone, rubric | `/infer`/`/ask`/`/feedback`, eval/cost/dashboard notebook, configs/logs | repository, 보고서, 발표, 재현성·품질·안전 평가 |
| 16 | 기말고사 — 팀별 프로젝트 결과 발표 | Capstone 결과·지표·한계·재현성 종합 | 팀별 demo와 발표 | 프로젝트 보고서+발표, 성적 30% |

## 격주 과제 축

Notion 커리큘럼의 기본 과제 흐름은 다음과 같다.

- 02주차: Prompt Variation 성능 비교
- 04주차: 문서 embedding 기반 QA notebook
- 06주차: LoRA Before/After 비교
- 10주차: 응답 log의 길이·시간·비용 분석
- 12주차: Multi-Agent/Tool workflow
- 14주차: Token cost 추정 CSV와 시각화

실제 강의자료에서는 09–10주차를 `Mini Chatbot API + LLMOps 로그 수집` 통합 과제로 구체화했고, 11·13·14주차에도 별도 실습 패키지와 루브릭이 추가되었다.

## 운영·평가 공통 기준

| 축 | 대표 지표·증거 |
|---|---|
| Quality | 정확성, EM/F1, Soft Match, usefulness, groundedness, faithfulness |
| Retrieval | Recall@k, Precision@k, MRR, NDCG, citation accuracy |
| Operations | latency p50/p95/p99, throughput, error rate, retry, cache hit rate |
| Cost | input/output tokens, request cost, monthly budget, model-routing 절감 |
| Safety | PII leak, toxicity, jailbreak ASR, blocked/allowed reason, audit log |
| Reproducibility | environment, config, prompt/model/data version, commit, README |

## 기준 자료

- [공개 Notion 메인 페이지](https://synonymous-faucet-52e.notion.site/AI-10-LLMOps-260a18c366b180deb569f134e48e7bff)
- [Notion 주차별 커리큘럼](https://synonymous-faucet-52e.notion.site/260a18c366b180d78d81d435d43a8043)
- [기존 실습 저장소](https://github.com/smilesjcha/ajou-llmops-2025-2nd-semester) — `main@554898da07d58b191066a94f37f0a9502138fe94`
- [기존 실습 저장소 강의계획 README](https://github.com/smilesjcha/ajou-llmops-2025-2nd-semester/blob/main/README.md) — Week08 중간고사·Week16 기말고사 근거
- 이 폴더의 `[AI_PR_PR_10] 01–07, 09–15` PPTX/PDF 원본

Notion 연결 앱은 이 공개 사이트가 속한 워크스페이스에 직접 접근하지 못해, 공개 페이지와 하위 페이지를 읽기 전용 브라우저로 확인했다. 개인 페이지와 학생 이력서 페이지는 수집 범위에서 제외했다.
