# Langfuse·LangSmith의 역할과 실제 실습 범위

**요청 추적·평가 데이터·실험 비교·검토 기록은 LLMOps의 핵심 기능입니다.** 특정 제품만이 필수인 것은 아니지만, 이번 수업은 원리와 실제 운영 도구를 연결하기 위해 Langfuse를 직접 실행합니다.

| 단계 | 실제 수행 | 경계 |
|---|---|---|
| 01–06 | TF-IDF 검색·지표·보고서 | 05의 judge 표는 작성 예시 |
| 07–08 | Ollama 생성·모델 평가·로컬 기록 | 이 파일들만으로 플랫폼에 전송하지 않음 |
| 09 | Docker Langfuse + SDK, trace·점수·서버 재조회 | 로컬 프로젝트에 합성 사례 전송 |
| 10 | 실제 Datasets·Experiments·A/B/C 비교·배포 조건 | 작은 회귀 사례, 운영 배포·롤백 없음 |
| LangSmith | 같은 기능을 설명하는 비교 사례 | 별도 계정 연결·전송 미실행 |

## 같은 개념의 대응

| 기능 | Langfuse 실제 실습 | LangSmith 개념 |
|---|---|---|
| 요청 원인 분석 | Trace / observations / 입력·출력·토큰 | Run trace / child runs |
| 기준 데이터 | Dataset item / 참고 기준 / source trace | Dataset example |
| 변경 비교 | 같은 데이터의 A/B/C Experiments | Experiments |
| 평가 근거 | 코드 Scores / 실제 judge / 사람 검토 | Feedback / annotation queue |

07–08의 `traces.jsonl`은 교육용 로컬 형식이며 제품 직접 업로드 포맷이 아닙니다. 09–10은 실제 Langfuse SDK의 OpenTelemetry 기반 관찰 전송과 Scores API를 사용합니다. 연결 주소는 로컬로 제한하고 별도 `.env`의 키만 읽습니다.

## 왜 세 버전을 비교하는가

A는 현재 동작의 기준선, B는 프롬프트 개선, C는 서비스 기능 정책입니다. “정책 안내”만 구현한 서비스가 “실시간 재고 조회” 기능까지 제공하는 것처럼 답하지 않도록 C에서 기능 경계를 적용합니다. 이는 모의 LLM 응답이 아니라 실제 서비스 코드의 분기이며, 이 경로는 모델을 호출하지 않았다고 기록합니다.

기능 유형은 UI 메뉴/API 라우트의 입력입니다. 정답·answerable을 읽어 분기하지 않으며 자유 문장 의도 분류기는 포함하지 않습니다. 정상 사례의 실제 LLM 호출과 경계 사례의 정책 응답을 같은 회귀 데이터에서 확인합니다.

## 수업에서 설치하는 것과 이후의 범위

- **이번에 실행:** Langfuse 로컬 서버, 실제 Ollama 호출, 요청·점수·실험 저장, 같은 질문의 비교, 배포 전 조건 검사.
- **학생이 판단:** 원문 근거와 답변의 의미 일치, 조건 누락, 모델 평가의 오판, 서비스의 제공 가능한 기능, 다음 변경.
- **이후 확장:** 운영 인증·권한·보관 정책, 실시간 재고 API, 더 독립적인 평가 모델, 대표 운영 데이터, CI 배포 파이프라인·롤백.

[Docker·VS Code 준비와 100분 시간표](langfuse/README.md)에서 시작합니다.

공식 자료: [Langfuse SDK](https://langfuse.com/docs/observability/sdk/instrumentation), [Scores](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk), [Experiments](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk), [LangSmith 평가 개념](https://docs.langchain.com/langsmith/evaluation-concepts). 확인일 2026-11-11.
