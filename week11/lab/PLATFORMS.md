# Langfuse·LangSmith가 필요한 이유와 실습 범위

**제품 설치는 선택이지만, 요청 추적·평가 데이터·실험 비교·검토 기록은 LLMOps의 핵심 기능입니다.** 초기 자료는 설치 없는 평가 계산에 집중해 실제 생성과 운영 도구의 연결이 부족했습니다. 개정판은 07–08의 실제 Ollama 호출과 제품 사례를 연결합니다.

| 기능 | 이번 실습 | Langfuse 사례 | LangSmith 사례 |
|---|---|---|---|
| 요청 원인 분석 | trace_id·단계별 spans·원응답 | Trace와 observations 탐색 | Run trace와 child runs 탐색 |
| 기준 데이터 | 질문·참고 답변·필수 문서 | Dataset item | Dataset example |
| 변경 비교 | baseline/grounded 프롬프트 | Experiments | Experiments |
| 평가 근거 | 코드 검사·실제 judge·사람 검토 | Scores·annotation | Feedback·annotation queue |

## 수업에서 필요한 자료

- **필수:** 서비스 아키텍처, 평가기의 입력과 출력, 실패 사례, 버전·지연 기록. ‘왜 틀렸는지’와 ‘변경 후 나아졌는지’를 설명하는 데 필요합니다.
- **사례로 필요:** Langfuse·LangSmith가 위 기록을 어떻게 검색·비교·검토하게 하는지. 도구 이름만 나열하지 않고 같은 실습 요청과 대응합니다.
- **이번 수업의 필수 범위 밖:** 두 제품의 동시 설치, 클라우드 계정 가입, 모든 SDK API, 서버 운영·과금·권한 체계. 실제 프로젝트의 협업·보관·보안 요구에 따라 하나를 선택하거나 다른 도구로 구현할 수 있습니다.

## 구현과 시연의 구분

| 대상 | 이번에 실행한 것 | 수행하지 않은 것 |
|---|---|---|
| 01–06 | 실제 TF-IDF 검색, 지표, bootstrap, 보고서 | 실제 답변 생성 |
| 05 | 작성 예시의 평가자 일치율 계산 | 실제 모델 판정 |
| 07 | 로컬 모델의 실제 검색 기반 답변·지연·토큰 | 신경망 임베딩 검색 |
| 08 | 실제 모델 판정·기준과 비교·로컬 trace | Langfuse·LangSmith로 전송 |
| 강의의 제품 화면 | 공식 문서의 Langfuse UI 사례 | 수업 계정에서 실행했다고 주장하지 않음 |

`traces.jsonl`은 학습용 로컬 형식입니다. 제품의 직접 가져오기 파일이나 OpenTelemetry 전송 규격이 아닙니다. 연결하려면 공식 SDK로 입력·출력·부모 작업·모델 버전·점수를 매핑해야 합니다. 현재 코드는 키를 읽거나 외부 추적 서비스로 데이터를 전송하지 않습니다.

## 프로젝트 적용 순서

1. 같은 질문의 두 버전을 로컬에서 실행하고 실패 원인을 설명합니다.
2. 기록해야 할 입력·출력·모델·프롬프트 버전·지연·평가 근거를 확정합니다.
3. 팀 단위 검색·공유·검토가 필요해지면 플랫폼을 선택합니다.
4. 공개 가능한 시연 데이터로 SDK 연결을 확인한 뒤 접근 권한·보관 정책을 설정합니다.
5. 운영 사례를 검토하여 회귀 평가 세트로 추가합니다. 실패 사례와 대표 정상 사례를 함께 유지합니다.

## 공식 참고 자료

- [Langfuse 관찰·추적](https://langfuse.com/docs/observability/overview)
- [Langfuse 평가](https://langfuse.com/docs/evaluation/overview)
- [Langfuse 실험 SDK](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)
- [LangSmith 평가 개념](https://docs.langchain.com/langsmith/evaluation-concepts)
- [MLflow 평가 실행 구성](https://mlflow.org/docs/latest/genai/eval-monitor/)
- [OpenTelemetry trace 개념](https://opentelemetry.io/docs/concepts/signals/traces/)

확인일: 2026-11-11. 특정 제품을 유일한 업계 표준이나 필수 기술로 지정하지 않습니다.
