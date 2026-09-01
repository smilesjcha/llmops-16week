# AS-IS 2025년 2학기 LLMOps 주차별 통합 강의안

## 사용 방법

이 문서는 Notion의 커리큘럼·하위 콘티, 실제 PPTX/PDF, 기존 notebook을 주차별로 합친 강의 운영본이다. 각 주차는 다음 순서로 정리한다.

1. 학습목표
2. 이론·슬라이드 흐름
3. 실습 시나리오
4. 과제·평가 증거
5. AS-IS 주의점

슬라이드의 문구를 장별로 검색해야 할 때는 `03_AS-IS_슬라이드_텍스트_원문.md`를 사용한다. 아래 슬라이드 범위는 실제 PPTX/PDF를 기준으로 하며, Notion의 초안 장수와 다를 수 있다.

---

## 01주차 — Orientation 및 LLM Lifecycle

- 실제 자료: 84장
- Notion: [1주차 강의](https://synonymous-faucet-52e.notion.site/1-260a18c366b180489b01c06f0c2e4ab7)
- 실습: `practice/week01/week01_ollama_practice.ipynb`

### 학습목표

- AI·딥러닝·Transformer·LLM의 발전 흐름을 설명한다.
- SFT, RLHF, DPO, PEFT가 post-training에서 맡는 역할을 구분한다.
- DevOps, MLOps, LLMOps의 공통점과 차이를 설명한다.
- LLM 서비스의 5단계 개선 순환과 이번 학기 전체 주차를 연결한다.
- 로컬 개발환경과 Ollama 기반 첫 LLM 호출을 완료한다.

### 이론·슬라이드 흐름

1. **수업·교수·평가 안내(s.3–15)**
   - 교수 경력, 수업의 프로젝트 성격, 운영 규칙과 평가방식
   - 한 학기 산출물이 개별 실습에서 Capstone으로 누적된다는 점을 강조
2. **AI 역사와 전환점(s.17–40)**
   - 상징적 AI 역사 → 머신러닝/딥러닝 → 대규모 데이터·GPU → Transformer
   - 연대기 암기보다 “왜 다음 기술이 필요했는가”에 초점
3. **LLM과 post-training(s.41–51)**
   - Pretraining 이후 SFT, RLHF, DPO, PEFT의 위치
   - 범용 모델을 태스크·도메인·선호에 맞추는 과정
4. **DevOps → MLOps → LLMOps(s.52–60)**
   - 코드 운영, 데이터·모델 운영, 프롬프트·응답·평가 운영으로 관심사가 확장되는 과정
5. **LLM Lifecycle(s.61–67)**
   - `기획/데이터 → 프롬프트 → 실행/배포 → 평가/모니터링 → 개선/버전관리`
   - “LLM Lifecycle: 지속적인 개선의 순환”을 학기 전체의 기준 그림으로 사용
6. **환경 세팅과 첫 실습(s.69–82)**
   - VS Code/Cursor, Python 3.11.13, venv, requirements, GitHub 주차 구조, Ollama

### 실습 시나리오

1. Python 가상환경을 만들고 의존성을 설치한다.
2. Ollama와 기본 모델(원본 notebook 기본값 `llama3.1:8b`)을 준비한다.
3. Chat API 연결 상태를 확인한다.
4. 요약, Q&A, 스타일 변환을 각각 호출한다.
5. temperature 등 파라미터를 바꾸고 응답·지연·설정을 CSV에 기록한다.
6. `practice/week01/results.csv`와 본인 실행 결과를 비교한다.

### 과제·평가 증거

- 실행 가능한 환경과 재현 절차
- 최소 3종 prompt 실행 결과
- model/parameter/latency/output이 포함된 로그
- 오류가 날 때 환경, 모델명, 실행 위치를 설명한 README

### AS-IS 주의점

- Notion 페이지는 표지와 목차 앞부분까지만 작성된 미완성본이다. 실제 강의 흐름은 PPTX/PDF를 기준으로 복원했다.
- s.13의 일부 본문은 PPTX 일반 텍스트보다 PDF 검색 텍스트가 더 잘 잡힌다.

---

## 02주차 — PromptOps Basic

- 실제 자료: 88장
- Notion: [2주차 강의](https://synonymous-faucet-52e.notion.site/2-268a18c366b1808584f2f363af9d242a) / [강의 내용](https://synonymous-faucet-52e.notion.site/268a18c366b180b48c03f7d5f8c1d3cf)
- 실습: `practice/week02/01_basic_prompt_engineering.ipynb` 외 3개

### 학습목표

- Prompt Engineering과 PromptOps의 차이를 설명한다.
- 모델·비용·한도·context window를 고려해 prompt 실험을 설계한다.
- 기본, 추론 보조, orchestration, production 기법을 상황별로 선택한다.
- prompt를 template·version·evaluation·monitoring 단위로 관리한다.

### 이론·슬라이드 흐름

1. **PromptOps 정의와 필요성(s.4–9)**
   - 개별 문장 최적화가 아니라 template, version, evaluation, deployment, monitoring의 전 과정
   - 비용·품질·속도·재현성·감사추적을 확보하는 운영 체계
2. **모델·비용·한도(s.10–25)**
   - GUI vs API, input/output/cached token 단가
   - RPM, TPM, RPD, context window, Azure의 모델·지역별 quota
3. **PromptOps Cycle(s.26–33)**
   - 문제 정의 → 모델·비용 선정 → template → experiment → evaluation → version → deployment → monitoring
4. **Setup Layer(s.34–46)**
   - Persona, Tone, Format/JSON, delimiter, length, pre-warming, ask-for-context
5. **Reasoning Aids(s.47–61)**
   - Zero/Few-shot, CoT, Least-to-Most, Tree of Thoughts, ReAct, PAL
6. **Orchestration(s.62–74)**
   - Function/Tool Calling, Multiple Chains, Meta-Prompting, APE
7. **Safety & Branching(s.75–84)**
   - 감성 기반 분기, 금칙어·PII filter, retry/backoff, circuit breaker, fallback

Notion의 9장 cycle 콘티는 `문제정의 → 모델·비용 → 템플릿 → 실험 → 평가 → 버전 → 배포 → 모니터링 → 전체 요약`으로 구성되며, 실제 덱은 각 단계를 다수의 기법·코드 예시로 확장했다.

### 실습 시나리오

| Notebook | 핵심 실습 |
|---|---|
| `01_basic_prompt_engineering.ipynb` | persona, tone, delimiter, JSON, length, context 요청, 종합 비교 |
| `02_advanced_reasoning.ipynb` | Zero/Few-shot, CoT, Least-to-Most, ToT, ReAct, PAL |
| `03_advanced_integration.ipynb` | Tool Calling, Multiple Chains, Meta-Prompting, APE |
| `04_production_techniques.ipynb` | 감성 분기, filter, retry/backoff, circuit breaker, fallback |

각 notebook은 OpenAI 경로와 Ollama/로컬 경로를 병기한다. 동일 입력에 대해 prompt version과 model을 바꾸되, 출력 형식과 평가 기준은 고정해 비교한다.

### 과제·평가 증거

- 번역·요약·분류 중 한 task 선택
- Prompt Variation 3종과 설계 의도
- 동일한 입력 세트·동일 평가축으로 결과 비교
- 품질·latency·token/cost 또는 로컬 실행 자원 비교
- 가장 좋은 prompt를 선택한 근거와 다음 개선안

### AS-IS 주의점

- 가격·모델 순위·quota 표는 2025년 8–9월 시점의 역사적 자료이며 현재값으로 사용하면 안 된다.
- `02_advanced_reasoning.ipynb`에는 저장된 `SyntaxError`, `03_advanced_integration.ipynb`에는 저장된 `NameError` 출력이 있다. AS-IS 보존을 위해 notebook은 수정하지 않았다.
- s.86의 “2부: 실습”은 실제 코드 예시 뒤에 놓여 있다. 운영본에서는 s.35–84의 예제를 실습 구간으로 재배치한다.

---

## 03주차 — Prompt Evaluation & Version Management

- 실제 자료: 64장
- Notion: [3주차 강의](https://synonymous-faucet-52e.notion.site/3-26fa18c366b1806686f7d0b470c6694c) / [31장 상세 콘티](https://synonymous-faucet-52e.notion.site/26fa18c366b180ed8611e2d3495745d5)
- 실습: `practice/week03/prompt_eval_and_version_mgmt.ipynb`

### 학습목표

- LLM 프로젝트 유형에 맞는 offline/online 평가축을 설계한다.
- prompt SemVer와 dev/staging/production 배포 라벨을 정의한다.
- Notion–GitHub–Langfuse를 SSOT 관점으로 연결한다.
- Trace, Prompt, Dataset, Evaluation의 역할을 구분하고 A/B 평가를 실행한다.

### 이론·슬라이드 흐름

1. **10개 프로젝트 유형(s.8–19)**
   - 대화형 QA, 온라인/사전지식 RAG, 요약, 점수 채점, 상세 피드백, 이메일·문서, 코드, 이미지·영상 설명, 창작 보조
   - 각 유형의 입력/출력, 실패 위험, 테스트셋, 운영지표를 구분
2. **평가 지표(s.20–38)**
   - 정확도, EM/F1, Soft Match, groundedness, citation accuracy, factuality
   - 유용성, 톤, 형식, 구조화, 안전 gate, p95/p99, 비용, cache, 오류율
   - 코드 task는 테스트 통과율, 정적분석, 성능을 별도 평가
3. **버전·배포·SSOT(s.39–49)**
   - SemVer, 배포 label, Notion DB schema, Prompty, PR, artifact link
4. **Langfuse/LangSmith(s.50–58)**
   - Trace, Prompt, Dataset, Evaluation의 데이터 모델과 도입 전략
5. **실습(s.60–62)**
   - 회의 transcript를 사용한 v0.0.1→v0.0.2 개선과 dataset evaluation

Notion의 [V0.0.1](https://synonymous-faucet-52e.notion.site/20250915-V0-0-1-Prompt-26fa18c366b180f48227ec737fce4304)는 120단어 요약+Top-5 bullet을 요구한다. [V0.0.2](https://synonymous-faucet-52e.notion.site/20250915-Prompt-V0-0-2-26fa18c366b1806f9da0f37c576fa55d)는 `Decisions / Action Items / Key Discussion Points / Risks / Open Questions / Next Steps`로 구조화하고, 없는 owner/date는 `TBD`, PII 최소화, bullet 길이 제한을 추가한다.

### 실습 시나리오

1. 회의 transcript 2건 이상을 로드한다.
2. v0.0.1과 v0.0.2를 동일 데이터에 실행한다.
3. 구조 준수, 사실성, action item 완전성, 길이, latency/cost를 기록한다.
4. Langfuse trace와 dataset/run을 생성하거나, 연결이 없으면 로컬 JSON/CSV로 동일 schema를 남긴다.
5. `meeting_minutes_v0.1.prompty`, `v0.2.prompty`와 PR용 개선 로그를 만든다.

### 과제·평가 증거

- prompt version 2개와 차이 설명
- 평가 dataset과 rubric
- run 결과, 개선 전/후 지표
- Git commit/PR 또는 동등한 version history
- 실패 예시와 다음 version의 가설

### AS-IS 주의점

- notebook은 Langfuse/OpenAI에 외부 trace·dataset 생성 및 비용을 발생시킬 수 있으므로 이관 단계에서 실행하지 않았다.
- 실행 위치 기준이 혼재한다. transcript는 `week03/` 기준, Prompty 일부는 저장소 루트 기준이므로 README의 실행 경로를 따른다.

---

## 04주차 — Basic of RAG & VectorDB

- 실제 자료: 85장
- Notion: [4–5주차 허브](https://synonymous-faucet-52e.notion.site/4-5-276a18c366b180be88c5f70492f7fe21)
- 최종 콘티: [1–2](https://synonymous-faucet-52e.notion.site/1-2-276a18c366b1800e8ffadb6484b759b5) → [3–4](https://synonymous-faucet-52e.notion.site/3-4-276a18c366b1807c85c2c9e0cfe41bcf) → [5–6](https://synonymous-faucet-52e.notion.site/5-6-276a18c366b180fd91fce68515ecb338) → [실습 준비](https://synonymous-faucet-52e.notion.site/276a18c366b1805e83c5ef810f9a8fe2)
- 실습: `practice/week04/RAG_Kor_Pinecone_QuickLab.ipynb`

### 학습목표

- RAG가 LLM의 최신성·근거·환각 문제를 어떻게 완화하는지 설명한다.
- corpus, chunk, embedding, ANN, VectorDB, retriever, augmentation, generation의 역할을 구분한다.
- 한국어 문서의 구조를 보존하는 chunk·metadata 전략을 설계한다.
- retrieval 결과를 Recall/MRR/NDCG 관점으로 평가한다.

### 이론·슬라이드 흐름

1. **RAG 정의·역사·7단계 파이프라인(s.4–25)**
   - 문제상황, 원전, corpus 준비, chunk, metadata, embedding, retrieval, prompt augmentation, grounded generation
   - RAG와 fine-tuning의 역할 차이
2. **Embedding·ANN·VectorDB(s.26–37)**
   - cosine/dot/L2, exact vs approximate search
   - HNSW, IVF, PQ, OPQ, hybrid·multi-vector·multimodal
   - VectorDB가 index 외에 filter, scale, backup, RBAC, monitoring을 맡는 이유
3. **모델·chunk·metadata 설계(s.38–49)**
   - MTEB, embedding dimension/normalization
   - 크기·overlap, 표/목록/제목 보존, 날짜·권한·출처 metadata
4. **한국어 데이터·국내 사례(s.50–62)**
   - KorQuAD, AI Hub 금융·법률 MRC, 모두의 말뭉치, ETRI Exobrain
   - 라이선스·개인정보·도메인 버전 관리
5. **평가·리스크(s.63–74)**
   - Recall, MRR, NDCG, RAGAS 계열 평가, latency/cost, stale document, retrieval leakage
6. **40분 Quick Lab(s.76–80)**
   - KorQuAD 2.0 → multilingual MiniLM 384d → Pinecone Serverless → Top-k → Recall@5

### 실습 시나리오

1. KorQuAD 2.0 일부 샘플을 정규화한다.
2. 제목·본문·표 구조를 고려해 chunk와 metadata를 만든다.
3. sentence-transformers로 embedding한다.
4. Pinecone에 upsert하거나, 무료 경로에서는 FAISS/Qdrant Local로 대체한다.
5. 질문별 Top-k 문서와 score·metadata를 확인한다.
6. gold document 기준 Recall@5를 계산하고 실패 질의를 분석한다.

### 과제·평가 증거

- PDF/텍스트 1개 이상과 chunk 정책
- embedding/index 설정
- 질문·gold evidence·Top-k 결과
- Recall@k와 실패 사례 3개 이상
- 출처가 포함된 답변 생성 또는 retrieval-only 분석

### AS-IS 주의점

- s.3의 상단 장 제목이 이전 주차의 `프롬프트 평가 및 Version 관리`로 잘못 남아 있다.
- Notion의 Google/Perplexity/ChatGPT/Claude 페이지는 조사 초안이다. 수치·사례는 최종 강의안 근거로 직접 승격하지 않고, 공식 문서·논문 검증 대상으로 분리한다.
- 그림 215개로 이미지 의존도가 높아 텍스트 원문만으로는 일부 비교표·도식 의미가 빠진다.

---

## 05주차 — Advanced RAG: Hybrid Search & Re-ranking

- 실제 자료: 61장
- Notion 우선본: [5주차 강의안 02](https://synonymous-faucet-52e.notion.site/5-02-27da18c366b1806dbda1e71af1fa83c1)
- 실습: `practice/week05/Hybrid_RAG_Pinecone_MIRACL_ko_ollama.ipynb`

### 학습목표

- BM25와 dense retrieval의 서로 다른 실패 유형을 설명한다.
- RRF와 weighted fusion을 선택·설정한다.
- Cross-Encoder reranker로 Top-N 후보를 Top-k로 재정렬한다.
- 한국어 도메인 문서의 구조·개정·권한 조건을 검색 pipeline에 반영한다.
- baseline 대비 retrieval 품질 향상을 지표로 입증한다.

### 이론·슬라이드 흐름

1. **문제와 baseline(s.4–12)**
   - Dense-only: 의미에는 강하지만 exact term·고유명사·조문 번호에 약함
   - BM25-only: lexical match에는 강하지만 paraphrase·의미 유사에 약함
2. **Part A — Hybrid(s.13–22)**
   - Dense+BM25, RRF, weighted α, BM25F, metadata allow-list
   - multi-vector, multimodal, latency/cost, fallback
3. **Part B — Re-ranking(s.23–30)**
   - Bi-Encoder retrieval vs Cross-Encoder pair scoring
   - Top-N/k 설정, 중복 제거, 상용·오픈소스 reranker 선택
4. **Part C — 한국어·임베딩 고급(s.31–38)**
   - 표/목록/조문, 약어, 개정일, 제목·본문·요약 분리
5. **Part D — 평가·리스크(s.39–52)**
   - Recall/MRR/NDCG, score calibration, hallucination·citation·stale data
6. **실습(s.54–58)**
   - MIRACL-ko, BGE-M3, Pinecone BM25Encoder, weighted/RRF, BGE reranker, Ollama

### 실습 시나리오

1. MIRACL 한국어 corpus/query를 준비한다.
2. BM25와 BGE-M3 dense index를 각각 구성한다.
3. sparse/dense baseline의 실패 질의를 분류한다.
4. weighted fusion과 RRF를 실행한다.
5. BGE reranker로 후보를 재정렬한다.
6. Recall/MRR/NDCG와 latency를 단계별로 비교한다.
7. 최종 근거를 Ollama 생성 prompt에 넣고 citation을 확인한다.

### 과제·평가 증거

- BM25-only, Dense-only, Hybrid, Hybrid+Rerank 네 조건
- 동일 query·gold set
- Recall/MRR/NDCG 및 latency 비교
- α, Top-N, k 선택 이유
- 가장 많이 개선된 query와 여전히 실패한 query 분석

### AS-IS 주의점

- Notion에는 40장 초안과 48장 개정본이 함께 있다. 통합본은 `강의안 02`의 문제→baseline→fusion→rerank→평가 흐름을 우선한다.
- notebook에는 `BAAI/bge-reranker-v2-m3` 로딩 `OSError`가 저장되어 있다. 모델 접근·cache·환경 문제를 확인한 뒤 재실행해야 한다.

---

## 06주차 — Fine-tuning I: SFT & LoRA

- 실제 자료: 48장
- Notion: [6–7주차 허브](https://synonymous-faucet-52e.notion.site/6-7-28da18c366b180959f56c42894b11e3e) / [6주차 32장 콘티](https://synonymous-faucet-52e.notion.site/6-01-28da18c366b180108201f22857dbf3e8)
- 실습: `practice/week06/06_lora_sft.ipynb`

### 학습목표

- Pretraining–SFT–Alignment–Serving의 관계를 설명한다.
- Instruction형과 Chat형 dataset schema를 설계한다.
- template, label masking, leakage, sequence packing의 실패 위험을 점검한다.
- LoRA/QLoRA의 rank, alpha, target module, quantization 선택을 설명한다.
- Base와 LoRA adapter의 품질을 동일 prompt set으로 비교한다.

### 이론·슬라이드 흐름

1. **SFT 목적과 데이터(s.4–17)**
   - 목적함수, teacher forcing, Instruction/Chat schema, template consistency
   - label masking, train/validation split, leakage, length·packing
2. **PEFT·LoRA·QLoRA(s.18–23)**
   - full fine-tuning 대비 parameter-efficient adaptation
   - rank/alpha/dropout/target module, 4/8-bit, NF4, memory trade-off
3. **인프라·재현성·평가(s.24–30)**
   - Transformers/PEFT/Accelerate/bitsandbytes, W&B/MLflow 선택
   - repo layout, config, seed, cost/time estimate, automatic/manual/LLM-as-Judge
4. **실습(s.32–41)**
   - TinyLlama, data validation, LoRA config A/B, train log, inference, Base-vs-LoRA 비교
5. **잘못 복제된 RAG 슬라이드(s.42–45)**
   - 05주차 s.55–58과 동일한 MIRACL/BGE/Pinecone 내용으로 본 주차 강의 흐름에서 제외

### 실습 시나리오

1. `data/train.jsonl` 80건과 `val.jsonl` 10건의 schema·길이·중복을 검사한다.
2. TinyLlama tokenizer와 chat/instruction template를 맞춘다.
3. 4/8-bit 옵션과 LoRA `r=8`, `alpha=16`, `q_proj/v_proj` 기준 설정을 확인한다.
4. 짧은 학습을 실행하고 loss, step, memory, time을 기록한다.
5. 고정 prompt 5–10개로 Base와 Adapter를 비교한다.
6. adapter, tokenizer, config, CSV 리포트를 보존한다.

### 과제·평가 증거

- dataset card와 leakage 점검
- 학습 config와 재현 seed
- adapter artifact
- Base-vs-LoRA 정량·정성 비교
- 과적합·형식 붕괴·환각 등 오류 taxonomy

### AS-IS 주의점

- notebook은 `week06/` 디렉터리 실행을 전제로 한다.
- `runs/lora_sft/`에 기존 adapter/checkpoint가 포함되어 있으며 AS-IS 산출물로 보존했다.
- s.42–45의 Hybrid RAG 복제본은 SFT 내용으로 통합하지 않는다.

---

## 07주차 — Fine-tuning II: DPO

- 실제 자료: 42장
- Notion: 7주차 별도 콘티 없음. [핵심 커리큘럼](https://synonymous-faucet-52e.notion.site/260a18c366b180d78d81d435d43a8043)과 6주차 예고만 존재
- 실습: `practice/week07/07_dpo.ipynb`

### 학습목표

- RLHF pipeline의 복잡성과 DPO의 동기를 설명한다.
- `prompt/chosen/rejected` preference pair의 품질 기준을 정의한다.
- DPO objective, β, reference policy, length bias의 의미를 설명한다.
- Week06 SFT adapter를 초기 policy로 사용해 DPO를 수행한다.
- Base/SFT/DPO를 품질·스타일·안전성 기준으로 비교한다.

### 이론·슬라이드 흐름

1. **Alignment spectrum과 RLHF 한계(s.4–8)**
   - SFT 이후 preference alignment의 필요성
   - reward model/PPO의 비용·불안정·복잡성을 DPO가 단순화하는 방식
2. **DPO 개념·수학·데이터(s.9–18)**
   - chosen/rejected log-probability 차이, reference policy, β
   - preference pair 작성, template consistency, length·position bias
3. **TRL 구현·평가(s.19–30)**
   - `DPOTrainer`, token length, batch/LR, checkpoint
   - automatic metric, pairwise judge, human review, safety metric 분리
4. **실습(s.32–39)**
   - preference demo data, Week06 adapter, β A/B, baseline/DPO inference, CSV/Langfuse

### 실습 시나리오

1. 120쌍 내외의 preference demo 또는 `prefs.jsonl`을 준비한다.
2. prompt/chosen/rejected 형식과 길이 편향을 검사한다.
3. Week06 adapter를 로드하거나 동일 base model을 기준으로 삼는다.
4. β 0.1, LR 5e-6, max length 256을 출발점으로 짧게 학습한다.
5. β A/B와 Base-vs-DPO를 동일 10문항으로 비교한다.
6. 유용성·스타일·거절·안전성을 구분해 기록한다.

### 과제·평가 증거

- preference dataset 설명과 금지 패턴
- DPO config와 reference policy
- pairwise 비교표
- 개선과 부작용을 함께 기술한 리포트
- checkpoint 또는 adapter와 재현 절차

### AS-IS 주의점

- Notion에는 7주차 상세 페이지가 없어 실제 PPTX/PDF와 notebook을 기준으로 통합했다.
- notebook은 저장소 루트 실행을 전제로 하며, Week06 adapter 경로를 직접 참조할 수 있다.

---

## 08주차 — 중간고사

### 근거와 운영

- Notion 주차별 커리큘럼과 주차 페이지에는 항목이 없다.
- 별도 PPTX/PDF와 notebook은 없다.
- 그러나 01주차 실제 강의자료의 학기 일정표와 [기존 실습 저장소 README](https://github.com/smilesjcha/ajou-llmops-2025-2nd-semester/blob/main/README.md)가 모두 Week08을 `중간고사`로 명시한다.
- 실제 강의자료 평가표는 `대면 객관식 30문항`, 성적 반영 `30%`, 오픈북 아님으로 안내한다.

### 평가 범위 정리 원칙

별도 시험지·정답·공지 원문은 이 폴더에 없으므로 구체 문항을 재구성하지 않는다. 01–07주차의 LLM lifecycle, PromptOps, 평가·버전, RAG, LoRA, DPO 핵심 개념과 실습 원리를 시험 범위의 AS-IS 기반으로만 연결한다.

---

## 09주차 — Inference Optimization & FastAPI

- 실제 자료: 82장
- Notion: [9주차 강의](https://synonymous-faucet-52e.notion.site/9-298a18c366b18057bbd8c9ffed46b5e3) / [1–30p](https://synonymous-faucet-52e.notion.site/1-30-page-298a18c366b180718854f05187e58400) / [31–60p](https://synonymous-faucet-52e.notion.site/31-60-page-298a18c366b1801ea11be579d8408c51)
- 실습: `practice/week09/09_fastapi_inference_lab.ipynb`와 `week09_app/`

### 학습목표

- 추론 latency를 queue, compute, network, post-processing으로 분해한다.
- quantization, KV/response/RAG cache의 적용 조건을 비교한다.
- OpenAI, GGUF/llama.cpp, vLLM/TGI/Ollama serving pattern을 구분한다.
- FastAPI/ASGI/async와 GIL의 영향을 고려해 API를 설계한다.
- SLI/SLO/SLA와 load test로 서비스 성능을 검증한다.

### 이론·슬라이드 흐름

1. **Quantization·GGUF·cache(s.6–17)**
   - Q4/Q5/Q8의 memory/quality/speed trade-off
   - KV cache와 response/RAG cache, cache key와 invalidation
2. **FastAPI·ASGI·async(s.18–30)**
   - endpoint, Pydantic schema, Uvicorn/Hypercorn, sync vs async I/O
3. **GIL과 concurrency(s.31–39)**
   - I/O-bound, CPU-bound, GPU-bound
   - ThreadPool, ProcessPool, multiprocessing 선택
4. **Production architecture(s.40–47)**
   - Nginx/ALB, stateless API, Redis, VectorDB, Celery/queue, worker
5. **API client·문서화(s.48–52)**
   - OpenAPI/Swagger, Postman, Insomnia, httpx
6. **SLI/SLO/SLA·Load Test·Scaling(s.53–63)**
   - p50/p95/p99, throughput, error rate, Locust/k6/wrk, load balancing
7. **Serving·배포·운영(s.64–78)**
   - vLLM/TGI/Ollama, SSE/WebSocket, timeout/retry, JWT/OAuth2, rate limit, Docker/K8s/HPA/PDB

### 실습 시나리오

1. notebook이 생성·설명하는 `week09_app/main.py` 구조를 확인한다.
2. mock 또는 실제 LLM adapter로 `/chat`, `/health`를 실행한다.
3. async HTTP 호출, cache, token-bucket rate limit, SSE를 단계적으로 적용한다.
4. Postman/Insomnia collection으로 API contract를 검증한다.
5. Locust 또는 k6로 동시 사용자 수를 늘리며 latency·throughput·error를 기록한다.
6. 병목과 개선 전/후 결과를 README에 남긴다.

### 과제·평가 증거

- 실행 가능한 Mini Chatbot API
- request/response schema와 오류 처리
- 부하테스트 설정·결과
- p50/p95/p99, throughput, error rate
- cache/rate limit/streaming 중 선택 기능

### AS-IS 주의점

- s.37은 실제 빈 슬라이드다.
- s.80 “2부: 실습”은 실습 설명 뒤에 있으므로 운영 순서에서는 앞당긴다.
- notebook은 앱 파일 생성·서버 실행·부하테스트를 포함하므로 자동 실행하지 않았다.

---

## 10주차 — LLMOps Stack

- 실제 자료: 89장
- Notion: [10주차 강의](https://synonymous-faucet-52e.notion.site/10-29fa18c366b18006aa70cdf580153cf1)
- 우선 콘티: [1–20p 디자인 02](https://synonymous-faucet-52e.notion.site/1-20p-02-29fa18c366b180388a15f84012f16f28) → [21–40p ver02](https://synonymous-faucet-52e.notion.site/21-40p-ver02-29fa18c366b18061b392f91e058bfaf0) → [41–60p](https://synonymous-faucet-52e.notion.site/41-60p-29fa18c366b180f1b5e9d8ae781f7b27) → [61–80p](https://synonymous-faucet-52e.notion.site/61-80-29fa18c366b180f08191fda6bc10f7a6)
- 실습: `practice/week10/week10_llmops_practice.ipynb`

### 학습목표

- DevOps–MLOps–LLMOps의 진화와 공통 운영 원리를 설명한다.
- 클라우드·오픈소스 도구를 기능별로 배치한다.
- LLM 호출의 공통 log schema를 설계한다.
- Langfuse 또는 CSV fallback으로 latency/tokens/cost/error/quality를 분석한다.
- 로그의 PII·retention·RBAC와 비용/SLA를 함께 고려한다.

### 이론·슬라이드 흐름

1. **MLOps/LLMOps 비교(s.4–23)**
   - model/data lifecycle과 prompt/response/evaluation lifecycle
   - trace, prompt version, model version, latency, tokens, cost, error, feedback
2. **서비스·도구 지도(s.24–39)**
   - Azure ML/AI Foundry, SageMaker/Bedrock, Vertex/Gemini
   - MLflow, Langfuse, W&B, DVC, Airflow/Prefect, vLLM/TGI/Ollama
3. **운영 지표(s.40–44)**
   - latency, token/cost, error, quality, RAG document/score
4. **실습·과제(s.45–60)**
   - Langfuse trace, CSV fallback, FastAPI logging hook, analysis, report, rubric
5. **보안·비용·SLA·배포(s.61–84)**
   - PII masking, retention, RBAC, budget dashboard, SLA, cloud/on-prem/hybrid
6. **Capstone 사전조사(s.85)**
   - 다음 주차들의 평가·보안·비용 지표를 Capstone proposal에 반영

### 실습 시나리오

1. OpenAI 또는 대체 local model을 5–10회 호출한다.
2. `timestamp, request_id, prompt_version, model, latency_ms, input_tokens, output_tokens, cost, status, feedback`를 기록한다.
3. Langfuse가 있으면 trace/span을, 없으면 CSV logger를 사용한다.
4. prompt version 2개를 실행해 latency/tokens/품질을 비교한다.
5. 09주차 FastAPI에 logging hook을 연결하는 확장안을 적용한다.

### 과제·평가 증거

[9–10주차 통합 과제](https://synonymous-faucet-52e.notion.site/9-10-2a0a18c366b180d8b06ff21aa421da6d)는 다음을 요구한다.

- `POST /chat` 기반 실제 또는 local LLM 호출
- CSV 또는 Langfuse log
- 6회 이상 호출
- prompt version별 latency/token 비교
- 코드, 로그, 0.5–1페이지 분석 요약

### AS-IS 주의점

- s.3 상단 제목이 이전 주차의 `추론 최적화 및 FastAPI`로 잘못 남아 있다.
- 1–20p 초안·디자인 ver01·디자인 02가 공존한다. 통합본은 `디자인 02`를 우선한다.
- s.87 “2부: 실습”은 실습·과제 이후의 빈 구분에 가깝다.
- OpenAI/Langfuse 실행은 비용과 외부 trace 생성이 가능하므로 자동 실행하지 않았다.

---

## 11주차 — Synthetic Data & RAG Evaluation

- 실제 자료: 71장
- Notion: [11주차 강의](https://synonymous-faucet-52e.notion.site/11-2a7a18c366b18002a035fce8d56ae777)
- 연속 콘티: [개념·필요성](https://synonymous-faucet-52e.notion.site/Synthetic-Data-2a7a18c366b180a0b616e7c8f0d3489c) → [생성 전략](https://synonymous-faucet-52e.notion.site/GPT-4-vs-nlpaug-2a7a18c366b1800ab14fe81414395933) → [평가·실습·과제](https://synonymous-faucet-52e.notion.site/2a7a18c366b180c9b7b8e7f8609e58a7)
- 실습: `practice/week11/week11_rag_synthetic_eval.ipynb`

### 학습목표

- real data와 synthetic data의 장점·편향·distribution gap을 설명한다.
- 문서→Q&A, paraphrase, hard negative, synthetic label 전략을 선택한다.
- retrieval 평가와 generation 평가를 구분한다.
- Recall@k, Precision@k, MRR, NDCG, Faithfulness를 해석한다.
- 최소 retriever와 평가 loop를 직접 구현한다.

### 이론·슬라이드 흐름

1. **Synthetic Data 필요성·유형(s.4–24)**
   - data scarcity, privacy, long-tail, test coverage
   - 문서→Q&A, paraphrase, hard negative, label generation
   - 편향·오염·실제 분포 괴리와 human review
2. **생성 전략(s.25–35)**
   - GPT 계열, local LLM, nlpaug·rule 기반 경로
   - JSON schema, evidence field, 난이도·다양성 control
3. **RAG 지표(s.36–46)**
   - retrieval: Recall/Precision/MRR/NDCG
   - generation: factuality/faithfulness/answer relevance/citation
   - rule, human, LLM-as-Judge의 trade-off
4. **평가 pipeline(s.47–54)**
   - documents → vector/feature → search → QA gold set → evaluation loop → 비교
5. **실습·과제·report(s.55–67)**
   - TF-IDF+cosine baseline, Recall@1/3/5, nlpaug 선택, matplotlib, export

### 실습 시나리오

1. 5–20개 문단과 document ID를 준비한다.
2. 질문·정답·gold document ID가 포함된 QA 10개 이상을 만든다.
3. TF-IDF/cosine retriever를 baseline으로 구현한다.
4. Recall@1/3/5를 계산한다.
5. nlpaug 또는 paraphrase로 질문을 증강한다.
6. 증강 전/후 recall과 실패 query를 비교한다.
7. `documents.json`, `eval_qas.csv`, 그래프와 report를 내보낸다.

### 과제·평가 증거

- 데이터 생성 규칙과 검수 기준
- gold evidence가 있는 QA set
- retriever config와 평가 코드
- Recall@1/3/5 및 선택 지표
- 증강이 좋아진/나빠진 이유를 보여주는 사례

### AS-IS 주의점

- s.69 “2부: 실습”은 실제 실습·과제 설명 뒤에 있다.
- notebook은 `week11/` 디렉터리 실행을 전제로 한다.

---

## 12주차 — Agent Chaining

- 실제 자료: 78장
- Notion: [12주차 강의](https://synonymous-faucet-52e.notion.site/12-2aea18c366b18096a605ec60965b657e)
- 콘티: [1–20p](https://synonymous-faucet-52e.notion.site/1-20p-2aea18c366b18048b5d4d2a99e86393d) → [21–40p](https://synonymous-faucet-52e.notion.site/21-40p-2aea18c366b180bd980ac267944a7141) → [41–60p](https://synonymous-faucet-52e.notion.site/41-60P-2aea18c366b180ecaa68eded00b9b95f)
- 실습: `practice/week12/week12_agents_tools_memory_chains_langchain_langgraph_langfuse.ipynb`

### 학습목표

- Chain, Tool, Agent, Memory의 책임을 구분한다.
- LCEL/Runnable과 `invoke/stream` pattern을 사용한다.
- session별 memory와 Tool을 연결한 Agent를 구성한다.
- LangGraph의 State/Node/Edge로 분기·loop workflow를 표현한다.
- Langfuse trace/span으로 Agent 실행을 관찰한다.

### 이론·슬라이드 흐름

1. **환경·기본 Chain(s.11–18)**
   - package/env, chat model helper, basic chat, LCEL Runnable
2. **Memory(s.19–23)**
   - stateless 문제, `RunnableWithMessageHistory`, session store, history injection
3. **Tool·Agent(s.24–42)**
   - `@tool`, calculator/time/uppercase/summary
   - `create_agent`, messages input, ReAct, stream, Agent+Memory, error/safety
4. **LangGraph(s.43–56)**
   - StateGraph, State/Node/Edge, `ChatState`, `add_messages`, LLM node, rule-based Tool router
5. **Langfuse Observability(s.57–74)**
   - Trace, Span, metadata, callback, Chain/Agent/Graph 공통 관찰, 평가 확장

### 실습 시나리오

1. 기본 chat과 `prompt | model | parser` chain을 실행한다.
2. session별 history를 붙여 stateless/stateful 결과를 비교한다.
3. calculator와 server-time 등 Tool 2개 이상을 정의한다.
4. Agent가 Tool을 선택하는 ReAct 흐름을 확인한다.
5. `ChatState`와 Tool router node로 LangGraph를 구성한다.
6. Langfuse가 있으면 callback/trace를, 없으면 local event log를 연결한다.

### 과제·평가 증거

- Tool 2개 이상과 명확한 type/docstring
- Tool 선택 이유가 드러나는 Agent/Graph 실행 기록
- session memory 또는 state transition
- 오류·잘못된 Tool 호출 처리
- 실행 trace와 짧은 개선 리포트

### AS-IS 주의점

- Notion 콘티는 61–80p Langfuse 파트를 예고하지만 해당 하위 페이지가 없다. 실제 PPTX/PDF의 s.57–74로 보완했다.
- s.3 마지막 항목 `평가 파이프라인 → 실습 절차 → 과제 → 리포트 예시`는 11주차 잔여 문구다.
- LangChain/LangGraph API version 차이로 Memory·Agent 예제는 재실행 전 호환성 검토가 필요하다.

---

## 13주차 — Security & Safety

- 실제 자료: 67장
- Notion: [13주차 강의](https://synonymous-faucet-52e.notion.site/13-2b5a18c366b180779cb0e9ade567802c) — 제목 외 본문 없음
- 실습: `practice/week13/week13_security_safety_lab.ipynb`

### 학습목표

- Security, Safety, Privacy의 위협·통제를 구분한다.
- prompt injection, jailbreak, retrieval poisoning, tool injection을 threat model에 배치한다.
- PII masking, moderation, RAG label, rate limit의 다층 방어를 설계한다.
- red-team 공격성공률과 운영 SLI를 측정한다.
- audit log, incident response, RACI/DPIA를 적용한다.

### 이론·슬라이드 흐름

1. **용어·위협모델·규정(s.4–12)**
   - asset, actor, attack surface, abuse case, 개인정보·규정
2. **다층 방어(s.13–25)**
   - Safety Sandwich, system policy, input/output filter, least privilege, isolation, rate limit
3. **PII·FastAPI·RAG guard(s.26–35)**
   - 한국어 regex, moderation classifier, middleware, document safety label, audit schema
4. **Red Team·SLI(s.36–45)**
   - jailbreak/injection test set, Attack Success Rate, false positive/negative, latency overhead
5. **실습·과제(s.46–55)**
   - PII masking, Detoxify 선택, RAG label filter, safety pipeline, CSV log
6. **Governance(s.56–63)**
   - incident response, retention, RBAC, RACI, DPIA, change review

### 실습 시나리오

1. 전화번호·이메일·주민번호 pattern을 정의한다.
2. input/output PII masking과 moderation을 분리한다.
3. RAG document에 safety label을 붙여 retrieval filter를 적용한다.
4. 허용·거절 이유를 audit log에 기록한다.
5. 정상/공격 prompt set으로 ASR, 차단율, 오탐, latency를 계산한다.

### 과제·평가 증거

- PII/Detoxify/RAG 안전 filter 중 2개 이상
- red-team test set
- CSV audit log와 지표
- 우회 공격 1개 이상과 보완책
- 개인정보 최소화·보존기간 설명

### AS-IS 주의점

- Notion 상세 페이지가 비어 있어 실제 PPTX/PDF와 notebook을 기준으로 복원했다.
- s.6 제목이 `스트·템플릿`으로 잘려 있다.
- s.65 “2부: 실습”은 실습·과제 뒤에 있다.

---

## 14주차 — Cost Optimization & Auto Scaling

- 실제 자료: 67장
- Notion: [14주차 강의](https://synonymous-faucet-52e.notion.site/14-2b7a18c366b18075bc15d19b756bbea9) — 제목 외 본문 없음
- 실습: `practice/week14/week14_cost_autoscale_lab.ipynb`

### 학습목표

- request와 월간 workload의 token 비용을 계산한다.
- latency, throughput, concurrency의 관계를 설명한다.
- cache, batching, model routing, quantization의 절감 효과를 비교한다.
- HPA/KEDA, queue, scale-up/out, Spot/on-demand를 선택한다.
- 품질·안전·SLO를 유지하는 cost scenario를 설계한다.

### 이론·슬라이드 흐름

1. **비용식·성능(s.4–15)**
   - input/output token, request cost, monthly volume, latency/throughput/concurrency
2. **최적화·cache·batch·scaling(s.16–23)**
   - response/prompt/RAG cache, micro-batching, scale-up/out, HPA/KEDA
3. **SLI/SLO/SLA와 비용 log(s.24–30)**
   - 비용·latency·error·quality의 공동 관찰
4. **압축·routing·guardrail·운영(s.31–53)**
   - prompt/context compression, small→large model escalation, queue/DLQ, dashboard, budget alert
5. **비용 추정 실습(s.54–63)**
   - `prompts.csv`, tiktoken, per-request/monthly cost, p50/p95/Top-N, cache what-if, scenario summary

### 실습 시나리오

1. 20–50개 prompt의 input/output token을 계산한다.
2. 모델 단가와 요청량으로 request·daily·monthly cost를 추정한다.
3. p50/p95와 비용 Top-N 요청을 시각화한다.
4. cache hit rate, model mix, prompt compression을 바꿔 2–3개 시나리오를 만든다.
5. 처리량·latency 가정으로 필요한 replica/worker를 추정한다.
6. 비용 절감이 품질·SLO를 훼손하는 조건을 명시한다.

### 과제·평가 증거

- 원본 prompt CSV와 단가·traffic 가정
- per-request cost와 monthly summary
- 시각화 2종 이상
- base/optimized scenario 비교
- 품질·안전·SLO guardrail

### AS-IS 주의점

- Notion 상세 페이지가 비어 있어 실제 PPTX/PDF와 notebook을 기준으로 복원했다.
- 일부 절감률·사례 수치는 출처·가정이 표시되지 않은 예시값이다. 현재 운영값으로 인용하지 않는다.
- s.65 “2부: 실습”은 실습·과제 뒤에 있다.

---

## 15주차 — Capstone Project

- 실제 자료: 76장
- Notion: 별도 주차 페이지 없음. [핵심 커리큘럼](https://synonymous-faucet-52e.notion.site/260a18c366b180d78d81d435d43a8043)의 `Capstone 설계 워크숍` 항목만 존재
- 실습 notebook: 없음

### 학습목표

- 문제·사용자·데이터·가설·KPI를 명확히 정의한다.
- 공통 API/log/config/evaluation contract를 적용한다.
- 품질(Q), 지연(L), 처리량(T), 비용(C), 안전(S)을 함께 측정한다.
- 재현 가능한 repository와 제출 패키지를 만든다.
- 팀별 기술 선택의 trade-off를 근거로 설명한다.

### 이론·슬라이드 흐름

1. **워크숍 목표·로드맵·역할(s.5–9)**
   - problem statement, team role, milestone, risk register
2. **Repo·data·log·KPI contract(s.10–23)**
   - 표준 디렉터리, dataset/version, 공통 로그, Q/L/T/C/S 지표
3. **API·구현 표준(s.24–44)**
   - `/infer`, `/ask`, `/feedback`, `/health`, `/metrics`
   - stateless FastAPI, cache/queue/batch, model adapter, safe RAG, config/CI, evaluation notebook
4. **7개 팀 project pattern(s.45–64)**
   - SLM vs LLM reranking
   - 반려동물 의료 Q&A 전문성 평가
   - 도서 추천 LLM monitoring
   - 논문 PDF 요약+Q&A
   - 보이스피싱/합성음성 탐지+법령 RAG
   - prompt 길이 vs 품질
   - GitLab Handbook chunk 전략×RAGAS
5. **완주 가이드·제출·rubric(s.65–74)**
   - milestone, demo, evidence, reproducibility, packaging, 발표

### Capstone 산출물

```text
project/
├── README.md
├── src/
├── configs/
├── tests/
├── logs/
├── 01_data/
├── 02_eval/
├── 03_cost_latency/
├── 04_dashboard.ipynb
├── report.pdf
└── slides.pdf
```

필수 증거는 baseline과 개선안, 고정 evaluation set, 품질·latency·cost·safety 지표, 실패 사례, 실행 명령, 환경·commit·config다.

### AS-IS 주의점

- s.3은 14주차 `Cost & Auto Scaling` agenda와 완전히 동일한 잘못된 복제본이다.
- s.4는 이미지 전용이라 검색 가능한 텍스트가 없다.
- Notion의 프로젝트 주제 관리에는 학생 이름·학번·이메일이 포함되어 있어 저장소로 이관하지 않았다. 위 7개 기술 주제만 비식별 수준으로 요약했다.

---

## 16주차 — 기말고사·팀별 프로젝트 결과 발표

- 별도 Notion 주차 페이지: 없음
- 별도 PPTX/PDF: 없음
- 별도 notebook: 없음
- 일정 근거: 01주차 실제 강의자료와 [기존 실습 저장소 README](https://github.com/smilesjcha/ajou-llmops-2025-2nd-semester/blob/main/README.md)

### 평가 목표

- 15주차에 합의한 문제·가설·API/log/KPI contract를 실제 결과로 입증한다.
- baseline과 개선안의 차이를 고정 evaluation set으로 설명한다.
- 품질·지연·처리량·비용·안전의 trade-off를 근거와 함께 발표한다.
- 다른 사람이 repository를 재현할 수 있도록 환경·config·commit·실행 명령을 제공한다.

### 팀별 발표 권장 순서

1. 문제와 사용자
2. 데이터·권한·전처리
3. baseline architecture와 지표
4. 개선 가설과 구현
5. 정량 결과(Q/L/T/C/S)
6. 대표 성공·실패 사례
7. demo
8. 재현 방법, 한계, 다음 단계

### 제출·평가 증거

- repository와 기준 commit
- README, config, environment/requirements
- evaluation dataset·notebook·result
- 운영 log와 dashboard 또는 분석표
- 최종 보고서와 발표 자료

실제 강의자료의 평가표는 기말 프로젝트를 `보고서 제출 + 발표`, 성적 반영 `30%`로 안내한다. 세부 rubric 원문은 15주차 Capstone deck의 제출·rubric 구간을 따른다.

---

## 공통 수업 운영 체크리스트

### 수업 전

- model/API/라이브러리 버전과 비용을 기준일과 함께 확인한다.
- `.env.sample`만 배포하고 실제 key는 commit하지 않는다.
- notebook의 실행 디렉터리와 외부 부작용을 공지한다.
- 고정 input/evaluation set과 expected artifact를 준비한다.

### 수업 중

- theory에서 정의한 지표를 practice log에 그대로 사용한다.
- 유료 경로와 무료/local fallback을 함께 제시한다.
- 성공 실행뿐 아니라 실패·오류·latency·cost를 기록한다.
- 화면 demo와 제출용 reproducibility를 구분한다.

### 수업 후

- prompt/model/data/config/commit version을 남긴다.
- 정량 지표와 대표 성공·실패 사례를 함께 제출한다.
- 개인정보·비밀·저작권이 포함된 artifact를 점검한다.
- 다음 주차가 재사용할 adapter/API/log/dataset을 명시한다.
