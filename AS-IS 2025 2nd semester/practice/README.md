# 2025년 2학기 LLMOps 실습 코드 — AS-IS

아주대학교 AI대학원 `AI융합실전프로젝트10`의 2025년 2학기 실습 코드와 실행 산출물을 원본 상태로 보존한 디렉터리다. 노트북 코드·출력·체크포인트를 수정하지 않았으므로, 당시 실행 결과와 오류 출력도 그대로 남아 있다.

원본 저장소와 기준 커밋, 포함·제외 범위는 [SOURCE.md](SOURCE.md)를 참고한다.

## 실행 전 확인

모든 노트북의 저장 커널은 Python `3.11.9`, 커널 표시 이름은 `ajou-llmops`다. 프로젝트 루트는 이 파일이 있는 `practice/` 디렉터리를 뜻한다.

```bash
cp .env.sample .env
```

필요한 키만 `.env`에 입력한다. `.env`는 Git에 커밋하지 않는다. 원본 `.env.sample`의 값은 실제 키가 아닌 placeholder다.

루트 `pyproject.toml`, `poetry.lock`, `requirements.txt`는 전체 16개 노트북의 모든 패키지를 포괄하지 않는다. 각 노트북의 설치 셀과 아래 의존성 표를 함께 확인해야 한다. 특히 Pinecone, OpenAI, Langfuse, PEFT, TRL, FlagEmbedding, scikit-learn 계열은 루트 명세에서 빠져 있거나 주차별로만 제시된다.

## 노트북 목록과 실행 기준

| 주차 | 노트북 | 제목·핵심 내용 | 권장 작업 디렉터리 | 주요 의존성·외부 자원 |
|---|---|---|---|---|
| 01 | `week01/week01_ollama_practice.ipynb` | Ollama 연결, Chat API, CSV 로깅, 요약·Q&A·스타일 변환·파라미터 실험 | `practice/week01` | `requests`, `pandas`, Ollama `llama3.1:8b` |
| 02 | `week02/01_basic_prompt_engineering.ipynb` | 문제 정의, persona, tone/format, delimiter·길이, pre-warming, context 요청 | `practice/week02` | `openai`, `python-dotenv`, Ollama CLI; `gpt-5-mini` |
| 02 | `week02/02_advanced_reasoning.ipynb` | zero/few-shot, CoT, Least-to-Most, ToT, ReAct, PAL | `practice/week02` | `openai`, `python-dotenv`, Ollama CLI; `gpt-5-mini` |
| 02 | `week02/03_advanced_integration.ipynb` | function/tool calling, multiple chains, meta-prompting, APE, 통합 시스템 | `practice/week02` | `openai`, `python-dotenv`, Ollama CLI; `gpt-4o-mini` |
| 02 | `week02/04_production_techniques.ipynb` | 감성 분기, 콘텐츠 필터, retry/backoff, circuit breaker, fallback | `practice/week02` | `openai`, `python-dotenv`, Ollama CLI |
| 03 | `week03/prompt_eval_and_version_mgmt.ipynb` | 회의 STT, prompt v0.0.1/v0.0.2, Langfuse trace·dataset·run·prompt version, Prompty | `practice/week03`¹ | `openai`, `langfuse`, `requests`, `python-dotenv`; `gpt-4o-mini` |
| 04 | `week04/RAG_Kor_Pinecone_QuickLab.ipynb` | KorQuAD 2.0 정규화·청킹·임베딩·Pinecone 검색·Recall@k | `practice/week04` | `pinecone-client>=5,<6`, `sentence-transformers`, `datasets`, `tqdm`; 선택 `ragas` |
| 05 | `week05/Hybrid_RAG_Pinecone_MIRACL_ko_ollama.ipynb` | MIRACL-ko, BM25+BGE-M3, dense/sparse/weighted/RRF, reranking, Ollama 생성 | `practice/week05` | `pinecone`, `pinecone-text`, `FlagEmbedding`, `datasets`, `rank_bm25`, `numpy`, `pandas`, `torch`, Ollama |
| 06 | `week06/06_lora_sft.ipynb` | Alpaca JSONL, TinyLlama, 4/8bit, LoRA SFT, Base/LoRA 비교, 결과 저장 | `practice/week06` | `transformers`, `datasets`, `peft`, `accelerate`, `bitsandbytes`, `sentencepiece`, `torch`, 선택 `langfuse`·Ollama |
| 07 | `week07/07_dpo.ipynb` | preference 데이터 생성, Week06 adapter, DPOTrainer, baseline/DPO 비교 | `practice`² | Week06 의존성 + `trl`; 선택 `week06/runs/lora_sft/adapter` |
| 09 | `week09/09_fastapi_inference_lab.ipynb` | FastAPI, SSE, 캐시, token bucket rate limit, Locust/k6, Postman/Insomnia | `practice/week09` | `fastapi`, `uvicorn`, `pydantic`, `httpx`; 선택 `redis`, `orjson`, Locust, k6 |
| 10 | `week10/week10_llmops_practice.ipynb` | OpenAI 호출, CSV/Langfuse logger, prompt-version 실험, 로그 분석 | `practice/week10` | `openai`, `pandas`, `python-dotenv`, `langfuse`; `gpt-4o-mini` |
| 11 | `week11/week11_rag_synthetic_eval.ipynb` | TF-IDF retriever, 합성/증강 Q&A, Recall@k, 시각화, 데이터 내보내기 | `practice/week11` | `pandas`, `scikit-learn`, `matplotlib`; 선택 `nlpaug`, `nltk` |
| 12 | `week12/week12_agents_tools_memory_chains_langchain_langgraph_langfuse.ipynb` | LangChain chat/chain, memory, tools, agent, LangGraph와 tool router | `practice/week12` | `langchain`, `langchain-core`, `langchain-openai`, `langgraph`, `langsmith`, `python-dotenv`, OpenAI |
| 13 | `week13/week13_security_safety_lab.ipynb` | PII 마스킹, 출력 모더레이션, RAG 안전 필터, 감사 로그와 시각화 | `practice/week13` | `pandas`, `matplotlib`; 선택 `detoxify`, `torch` |
| 14 | `week14/week14_cost_autoscale_lab.ipynb` | 토큰·비용 계산, 월 예산, cache/단가 what-if, 처리량·지연 시뮬레이션 | `practice/week14` | `pandas`, `matplotlib`; 선택 `tiktoken` |

¹ Week03은 원본 코드의 상대 경로 기준이 섞여 있다. STT 입력과 `datasets/` 출력은 `practice/week03` 실행이 맞지만, 마지막 Prompty 조회 셀은 프로젝트 루트 기준 `Path("week03/prompts")`를 사용한다. 원본 보존을 위해 수정하지 않았다.

² Week07 설정은 `week07/data`, `week07/runs/dpo`, `week06/runs/lora_sft/adapter`를 프로젝트 루트 상대 경로로 참조하므로 `practice/`에서 실행해야 한다.

원본에는 Week08·15·16 실습 노트북이 없다. Week08과 Week16은 시험, Week15는 Capstone 설계 워크숍에 해당한다.

## 주요 지원 파일

- Week01: `results.csv` — Ollama 실험 로그
- Week03: 회의 원문, transcript/summary 샘플, Langfuse dataset JSONL, Prompty v0.1/v0.2
- Week05: `artifacts/bm25_encoder.pkl`
- Week06: `data/train.jsonl`, `data/val.jsonl`, LoRA adapter, `checkpoint-5`, Base/LoRA 비교 CSV
- Week09: FastAPI 앱 모듈, 전용 requirements, `.env.sample`, Locust/k6, Postman/Insomnia 컬렉션
- Week10: `logs/llm_responses.csv`
- Week11: `week11_data/documents.json`, `week11_data/eval_qas.csv`
- Week13: `week13_logs/safety_log.csv`
- Week14: 입력 prompt CSV와 요청별 비용·시나리오 요약 CSV

Week03에는 동일한 `week03_meeting_minutes_demo.jsonl`이 `week03/datasets/`와 `week03/week03/datasets/`에 중복 보존되어 있고, `week03/week03/datasets/week03_meeting_minutes_pairs.jsonl`은 원본부터 0-byte 파일이다.

## 원본에 저장된 오류 출력

다음 오류는 가져오기 과정에서 발생한 것이 아니라 원본 노트북에 이미 저장되어 있던 실행 출력이다.

1. `week02/02_advanced_reasoning.ipynb`
   - `SyntaxError: unterminated string literal (detected at line 11)`
2. `week02/03_advanced_integration.ipynb`
   - `NameError: name 'ape_result' is not defined`
3. `week05/Hybrid_RAG_Pinecone_MIRACL_ko_ollama.ipynb`
   - `OSError: Can't load the model for 'BAAI/bge-reranker-v2-m3'`

AS-IS 재현을 위해 해당 출력과 관련 셀을 고치거나 제거하지 않았다.

## 외부 변경·비용 주의

노트북 전체 실행 전에 셀별 동작을 확인한다.

- Week01·02·05·06·07은 로컬 Ollama 프로세스와 모델을 사용할 수 있다.
- Week02·03·10·12는 OpenAI API 호출로 비용이 발생할 수 있다.
- Week03은 Langfuse dataset, trace, dataset run, prompt version을 원격에 생성할 수 있다.
- Week04·05는 Pinecone serverless index를 생성하고 vector를 upsert한다. Week04의 index 삭제 셀은 원본에서 주석 처리되어 있다.
- Week04–07은 Hugging Face 데이터셋·모델을 내려받고 상당한 네트워크, 디스크, CPU/GPU 메모리를 사용할 수 있다.
- Week05 설치 셀은 기존 `pinecone`, `pinecone-client`, `pinecone-plugin-inference`를 제거한 뒤 `pinecone`을 다시 설치한다. 공유 환경에서 바로 실행하지 않는다.
- Week06·07은 학습 결과와 checkpoint를 덮어쓸 수 있다. `bitsandbytes`와 4/8bit 설정은 OS·GPU 조합에 따라 동작하지 않을 수 있다.
- Week09는 로컬 API 서버, 선택적 Redis, Locust/k6 부하 테스트를 사용한다.
- Week10·13·14는 기존 CSV 로그·결과에 추가 기록하거나 파일을 다시 생성할 수 있다.
- Week12는 설정에 따라 LangSmith trace를 외부로 전송한다.

## 라이선스

원본 커밋에는 별도 라이선스 파일이 없다. 이 디렉터리는 원저작자의 강의 자료를 이관·보존한 것이며, 제3자 재사용이나 재배포 조건을 제공하지 않는다. 자세한 내용은 [SOURCE.md](SOURCE.md)의 라이선스 항목을 확인한다.
