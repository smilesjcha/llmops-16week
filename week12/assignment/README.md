# 12주차 과제03 · Langfuse 상담 AI 개선 미션

**개인 과제 · 2026년 12월 4일(금) 23:59 KST · LMS 제출 시도 최대 5회**

[공개 과제·작성 양식](https://smilesjcha.github.io/llmops-16week/week12/assignment/) · [과제 Notebook](01_langfuse_mission.ipynb) · [강의 마지막 장](https://smilesjcha.github.io/llmops-16week/week12/lecture/#slide-64)

11월 20일 수업 기준 2주입니다. 기존 11월 27일 마감과 02·04번 중심 과제 안내를 이 미션으로 대체합니다.

## 미션

정상 교환 질문과 실시간 재고 질문, 총 2개를 A baseline / B grounded 프롬프트에 각각 입력합니다. **실제 요청 4건, 모델 호출 8회**(답변 생성 4 + 모델 평가 4)를 실행한 뒤 Langfuse에서 근거·답변·점수를 읽습니다. B가 반드시 좋아져야 하는 과제가 아닙니다.

1. 실제 응답과 Trace 저장 확인.
2. A/B 답변·코드 검사·모델 판정·개별 지연 비교.
3. B의 재고 답변을 직접 읽고 사람 검토 점수·이유 기록.
4. 다음 변경 하나와 사용자 A/B 실험 계획 작성.

고정 질문의 A/B 비교는 온라인 사용자 실험이 아닙니다. 사용자 모집이나 실제 온라인 실험 수행은 요구하지 않습니다. 가상 ID로 고정 배정만 확인하고 실험 계획을 작성합니다.

## VS Code 준비

저장소 전체를 열고 기존 Python 3.11 `.venv`를 활성화합니다. Docker Desktop과 Ollama를 실행합니다. [처음 설치·로그인·문제 해결](../../week11/lab/langfuse/README.md)을 먼저 확인합니다. 초기 이미지·모델 다운로드는 과제 예상 시간과 별도입니다.

```sh
python -m pip install -r requirements/week12-langfuse.txt
python week11/lab/langfuse/init_env.py
ollama pull qwen2.5:1.5b-instruct
docker compose -f week11/lab/langfuse/compose.yaml up -d --wait --wait-timeout 300
```

로컬 Langfuse는 http://localhost:3011 입니다. `week11/lab/langfuse/.env`의 로그인 계정으로 접속합니다. API 키와 비밀번호를 출력하거나 제출하지 않습니다. 기존 11주차 프로젝트와 `week11-local` 환경을 재사용하며 `w12-mission-...` 세션 ID로 이번 실행을 구분합니다.

## Notebook 실행 순서

오른쪽 위 Select Kernel에서 저장소의 Python 3.11 환경을 선택하고 **코드 셀 1–8**을 위에서 아래로 실행합니다. 설치 후 예상 60–90분입니다.

| 코드 셀 | 확인할 결과 | 학습 내용 |
|---|---|---|
| 1–2 | 연결·모델·질문·비교 조건 | 9주차: 요청과 JSON 응답 계약 |
| 3–4 | 두 질문의 A/B 실제 응답과 Trace 링크 | 11주차: 같은 질문의 품질 비교 |
| 5 | 부모 1개 + 하위 작업 4개, 비교표·Scores | 10주차: 흐름·개별 지연 / 11주차: 점수 해석 |
| 6 | REVIEW·COMMENT 직접 작성 후 human_review 저장 | 모델 판정과 사람 검토의 구분 |
| 7 | 같은 가상 사용자에게 같은 버전, 계획 5항목 | 12주차: 사용자 배정·분모·보호 기준·종료 |
| 8 | evidence.json·comparison.csv 저장 | 근거 보존과 제출 |

9주차 내용은 기존 파이프라인의 Ollama HTTP 요청과 `answer`·`citations`·`abstain` 계약에서 확인합니다. 별도 FastAPI 서버나 Prometheus를 새로 띄우는 요구는 없습니다. 네 요청의 생성 시간은 개별 관찰값이며 p95나 일반 서비스 성능의 근거가 아닙니다.

## Langfuse 화면 확인

1. 셀 5의 **B Q24a 링크** → `01-retrieval` Output의 근거 → `02-ollama-answer` Input/Output의 실제 응답. Trace 트리·입출력 화면 1장 캡처.
2. 같은 요청의 **Scores** → 코드 검사·`llm_groundedness`·직접 작성한 `human_review`와 이유 비교. Scores 또는 A/B 비교표 화면 1장 캡처.

Trace는 한 요청 전체, Span/Observation은 내부 작업, Generation은 모델 호출 기록입니다. Score는 특정 기준의 평가값이며 정확도 전체를 뜻하지 않습니다. [공식 데이터 모델](https://langfuse.com/docs/observability/data-model) · [SDK 점수 기록](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)

## 제출물과 평가

**판단 메모 1–2쪽 PDF 또는 HTML + 근거 화면 2장**을 제출합니다. 캡처는 메모 안에 넣거나 별도 파일로 첨부해도 됩니다. Notebook·JSON 원본은 선택 첨부이며 HWP/HWPX는 제외합니다.

메모에는 결론(보류/추가 검토), 실제 답변·점수·시간의 근거, 다음 변경 하나, 사용자 A/B 설계와 한계를 적습니다. 실험 설계는 변경·배정 / 성공 지표와 전체 진입자 분모 / 보호 기준 / 기간·종료 규칙 / 확인 범위의 다섯 항목입니다.

| 평가 기준 | 배점 |
|---|---:|
| 실행 근거: 요청·Trace·응답 계약·개별 지연 | 30 |
| 품질 판단: 원문·코드·모델·사람 평가 비교 | 30 |
| 온라인 실험 설계: 배정·지표·분모·보호·기간 | 25 |
| 결론·다음 변경·읽기 쉬운 증거 | 15 |

아주대AI대학원은 [LMS 과제 바로가기](https://eclass2.ajou.ac.kr/ultra/courses/_118756_1/assessment/Test/_2542055_1?gradeitemView=details)의 **과제출제/제출 → 12주차 과제03 · Langfuse 상담 AI 개선 미션**에 제출합니다. 최대 5회이며 마감 전 수정본을 다시 제출할 수 있습니다. 군산대·국립창원대 및 그 외 수강생은 같은 기한까지 공지된 교수 이메일로 개인 제출합니다.

로컬 Trace URL은 다른 PC에서 열리지 않으므로 캡처를 첨부합니다. 공개 GitHub에 제출물을 올리지 않습니다. API 키·.env·비밀번호·다른 사람의 개인정보를 포함하지 않습니다.

설치가 끝내 해결되지 않으면 오류와 해결 시도, [공개 실제 실행 예시](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/langfuse/)로 분석한 범위를 구분해 제출합니다. 예시를 본인의 실행 결과로 표시하지 않으며 예시 분석만으로 직접 실행 항목이 충족되지는 않습니다.
