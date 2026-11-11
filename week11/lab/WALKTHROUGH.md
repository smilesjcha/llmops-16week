# 11주차 VS Code 실습 순서와 확인 결과

**자습 순서: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10** 순서로 진행합니다. 각 파일은 독립 실행됩니다. 01–08은 환경 준비 1개와 실험 6개, 09–10은 환경 준비 1개와 실험 8개입니다. 먼저 기본값으로 실행한 뒤 설정을 하나씩 바꿉니다.

**100분 실시간 수업에서는 모든 셀을 재실행하지 않습니다.** 01–08 핵심 발췌 후 09의 요청 추적과 10의 세 버전 비교를 중심으로 진행합니다. [수업 시간표·Docker 준비](langfuse/README.md)를 수업 전에 확인하세요.

## 1. 실행 준비

VS Code의 **File → Open Folder**에서 `llmops-16week` 폴더 전체를 엽니다. Python·Jupyter 확장을 설치하고, 새 터미널에서 실행합니다.

```sh
# macOS / Linux: 저장소 루트에서 실행
source .venv/bin/activate
python --version
python -m pip install -r requirements/week11-offline.txt
python -m pip check
```

기존 `.venv`가 없거나 Windows를 사용하는 경우 [환경 준비](README.md#vs-code-준비)를 먼저 따릅니다. Python은 **3.11.x**입니다. 01–06은 Ollama 없이 실행합니다. 07–08은 아래의 로컬 Ollama 준비가 필요하며 Docker·클라우드 API 키는 필요 없습니다.

각 Notebook의 **Select Kernel → Python Environments → 저장소 .venv**를 선택합니다. 해당 환경이 보이지 않으면 `.venv/bin/python`(Windows: `.venv\Scripts\python.exe`)을 지정합니다.

- 처음 따라 할 때: 첫 코드 셀부터 **Shift+Enter**로 한 셀씩 실행
- 전체 확인: **Restart Kernel → Run All**로 처음부터 실행
- 01–06의 첫 출력: `환경 준비 완료 3.11.x 문서 22 질문 48`
- `예상된 실패`, `누수 차단`, `형식 거부`는 의도한 검증 메시지입니다. 빨간 예외로 셀이 중단되는 것은 정상 결과가 아닙니다.

## 2. 파일별 확인 결과

아래 값은 **원본 데이터·기본 설정**의 2026-11-11 재실행 결과입니다. 소수점 마지막 자리와 실험 ID는 환경에 따라 달라질 수 있습니다. 01–06은 실제 TF-IDF 검색을 계산하며, 07–08에서 로컬 LLM 생성·평가를 추가합니다.

### 01. 평가 데이터의 기준과 분리

[01_dataset_contract.ipynb](notebooks/01_dataset_contract.ipynb)

| 실행 구간 | 확인 결과 | 이해할 핵심 |
|---|---|---|
| 현재·과거 문서 | 현재 18개, 과거 4개 | 유사한 문서라도 폐기된 정책은 정답 근거가 아님 |
| 평가 항목 구조 | Q03a의 `gold_ids = [D03, D04]` | 교환 기간과 비용에 문서 2개 필요 |
| 문항과 독립 의도 | dev/test 각각 24문항·12개 의도 | 표현 2개를 독립 의도 2개로 세지 않음 |
| 정답 무결성 | `예상된 실패: Invalid gold evidence / answerability` | 없는 문서 D999를 정답에 넣는 실수 차단 |
| 표현 변형 누수 | `누수 차단: Group leakage between dev and test` | 같은 의도가 개발·평가 양쪽에 섞이지 않도록 분리 |

**직접 확인:** Q03a가 왜 단일 정답이 아닌지 설명합니다. 오류 실험은 복사본만 바꾸며 원본 JSON은 수정하지 않습니다.

### 02. 검색 기준선과 원인 분리

[02_retrieval_baselines.ipynb](notebooks/02_retrieval_baselines.ipynb)

| 실행 구간 | 확인 결과 | 이해할 핵심 |
|---|---|---|
| 단어 단위 기준선 | D02 → D20 → D04 | 현재 문서와 폐기 문서가 함께 검색됨 |
| 벡터 크기 | `(22, 482)` | 문서 22개 × 단어/단어 조합 특징 482개 |
| 겹치는 단어 없음 | `[]` | 검색 결과 없음과 서버 오류는 다름 |
| 문자 검색 | `반품 배송비`, `반품배송비` 모두 D02가 1위 | 띄어쓰기 변화는 견뎌도 동의어는 놓칠 수 있음 |
| 한 요소씩 비교 | 아래 dev 비교표 | 버전 필터와 검색 방식의 효과 분리 |
| 동점 처리 | A → B | 같은 점수는 문서 ID로 순서 고정 |

| dev 설정 | Recall@3 | 구버전 포함 비율 | 답변 불가 수락률 |
|---|---:|---:|---:|
| word-all | 65.625% | 16.667% | 25% |
| word-current | 71.875% | 0% | 25% |
| char-current | 93.750% | 0% | 100% |

**직접 확인:** 마지막 행은 기권 임계값 0입니다. 검색 Recall이 높아져도 문서 밖 질문까지 수락한다는 점을 확인합니다. 04번의 임계값 적용 후 test 결과와 혼동하지 않습니다.

### 03. 지표 계산과 검색 개수

[03_metrics_and_k.ipynb](notebooks/03_metrics_and_k.ipynb)

| 실행 구간 | 확인 결과 | 이해할 핵심 |
|---|---|---|
| 정답 2개 중 1개 검색 | Hit=1, Recall=0.5 | 하나라도 찾기와 필요한 근거 모두 찾기의 차이 |
| 순위 `[X, A, B]`, 정답 `[A, B]` | MRR=0.5, nDCG≈0.693426 | 첫 정답 순위와 전체 관련 문서 순위의 차이 |
| 라이브러리 교차 검증 | nDCG 손계산과 sklearn 결과 일치 | `assert`를 오류 없이 통과 |
| 답변 불가 / 검색 실패 | 각각 `None` / `0.0` | 정의 불가와 0점 구분 |
| k=1, 3, 5 비교 | dev Recall 87.5%, 93.75%, 93.75% | k를 늘려도 계속 개선되지는 않음 |
| 중복 ID 입력 | `중복 차단: ...` | 정답 중복으로 점수 부풀리기 방지 |

**직접 확인:** `k=3`과 `k=5`의 차이가 없는 이유를 설명합니다. Hit는 검색 성공 여부, MRR은 Mean Reciprocal Rank(첫 정답 순위 역수 평균), nDCG는 normalized Discounted Cumulative Gain(정규화된 순위 할인 이득)입니다.

### 04. 기권 기준과 실패 분석

[04_calibration_and_error_analysis.ipynb](notebooks/04_calibration_and_error_analysis.ipynb)

1. **설정 선택:** `char-current-k3-t0.3` 확인. 문자 검색·현재 문서·k=3·임계값 0.3입니다.
2. **임계값 변화:** 값을 높이면 응답 시도가 줄어듭니다. 0.6에서는 dev의 모든 질문에 기권합니다.
3. **고정 test 비교:** 아래 네 지표를 함께 읽습니다.
4. **말투별 분석:** 답변 가능한 직접 질문의 Recall은 100%, 구어체는 62.5%입니다. 구어체의 답변 가능 질문은 모두 기권합니다.
5. **실패 추적:** Q02b·Q03b·Q05b의 질문, 필수 문서, 실제 검색 결과를 비교합니다.
6. **분리 규칙:** `test 선택 금지: Tuning accepts dev questions only`가 출력됩니다.

| test 지표 | 기준선 | 후보 |
|---|---:|---:|
| 검색 Recall@3 | 56.25% | 81.25% |
| 필수 근거 확보율 | 56.25% | 50.00% |
| 답변 불가 수락률 | 50.00% | 12.50% |
| 응답 시도 비율 | 62.50% | 37.50% |

**직접 확인:** Q05b는 필요한 D06을 검색했지만 최고 점수가 임계값보다 낮아 기권합니다. 검색 개선과 서비스 사용성 개선이 다를 수 있습니다. 임계값은 정답 확률이 아닙니다.

### 05. 답변 평가와 평가자 검증

[05_judge_rubric.ipynb](notebooks/05_judge_rubric.ipynb)

| 실행 구간 | 확인 결과 | 이해할 핵심 |
|---|---|---|
| 판정 기준 | supported / unsupported / uncertain | 근거로 뒷받침 / 충돌·부족 / 검토 필요 |
| 숫자 문자열 검사 | 반품 가능·불가 문장 모두 `True` | 같은 숫자가 있어도 의미는 반대일 수 있음 |
| 평가 요청 | 질문·근거·답변을 담은 프롬프트 출력 | 실제 LLM 호출은 수행하지 않음 |
| 결과 파싱 | supported JSON 통과, `좋음` 판정은 거부 | 형식 검증과 의미 검증은 별도 |
| 불일치 분석 | 5/8=62.5%, J03·J05·J06 불일치 | 불일치 원인 직접 읽기 |
| 순서 일관성 | 2/3≈0.666667 | 답변 순서를 바꿔도 의미상의 답변 ID가 같은지 확인 |

**직접 확인:** ‘불량 상품 반품 무료’를 ‘모든 반품 무료’로 바꾼 J03의 오류를 설명합니다. 위 수치는 **작성한 교육용 예시의 계산**이며 실제 모델 평가 결과가 아닙니다.

### 06. 비교 보고서와 배포 전 판단

[06_release_report.ipynb](notebooks/06_release_report.ipynb)

1. **전체 실행:** 기준선·후보 지표가 04번과 일치합니다.
2. **불확실성:** Recall 차이 +25.0%p, 그룹 bootstrap 95% 구간 +6.25~+43.75%p. 답변 가능한 의도 8개, 반복 2,000회입니다.
3. **개별 변화:** Recall이 개선되어도 `missed_answer`로 남은 질문을 확인합니다.
4. **배포 기준:** `HOLD`, 검증 조건 4개 중 2개 통과. 답변 불가 수락률과 필수 근거 확보율이 기준 미달입니다.
5. **HTML 보고서:** `week11/lab/reports/report.html`, `results.json` 생성.
6. **재현 확인:** 같은 환경에서 두 번 실행한 ID와 요약값이 일치해 `assert`를 통과합니다. 이번 재실행 ID는 `e6fdb3f8a0ff`입니다.

macOS 저장소 터미널에서 보고서를 엽니다.

```sh
open week11/lab/reports/report.html
```

브라우저에서 **선택된 후보 → 답변 불가 수락** 필터를 고르면 **Q24a 1건**이 나옵니다. **근거 보기**를 눌러 ‘현재 재고’ 질문에 교환 규정을 검색한 이유를 검토합니다. 필터 초기화 후에는 24문항입니다.

**HOLD는 정상 실행 결과입니다.** 배포 기준을 충족하지 못한 후보를 발견한 것입니다. `--enforce-gate` 옵션에서 종료 코드 2가 나오는 것도 의도한 차단입니다.

### 07. 실제 Ollama RAG 응답 비교

[07_ollama_rag_generation.ipynb](notebooks/07_ollama_rag_generation.ipynb)

**추가 준비:** Ollama 앱을 실행한 뒤 별도 터미널에서 아래 명령을 실행합니다. 다운로드는 최초 한 번입니다.

```sh
ollama pull qwen2.5:1.5b-instruct
ollama list
```

앱을 사용하지 않는 경우 별도 터미널에서 `ollama serve`를 유지합니다. 이미 서버가 실행 중이면 다시 띄우지 않습니다.

| 실행 구간 | 확인 결과 |
|---|---|
| 환경 준비 | 모델명·digest·Ollama 버전 출력. 없으면 pull 안내와 함께 중단 |
| 기준 응답 | Q01a의 검색 문서, 실제 answer·citations·abstain |
| 프롬프트 비교 | 같은 질문에서 baseline과 grounded의 실제 응답 비교 |
| 경계 질문 | Q03a 기간·비용·조건, Q24a 실시간 재고에 대한 기권 여부 |
| 검사 | 인용 ID·필수 근거·기권 일관성을 각각 확인 |
| 속도 | latency_ms, load_ms, input_tokens, output_tokens 확인 |
| 저장 | `reports/ollama-report.html`에 실제 생성 4건 저장 |

**중요한 관찰:** 확인 불가라는 문장인데 `abstain=false`일 수 있고, 올바른 문서를 인용했어도 기간을 누락할 수 있습니다. 코드 검사 통과를 답변 정확성으로 해석하지 않습니다. 문장은 실행마다 달라질 수 있으며 오류를 가짜 정답으로 대체하지 않습니다.

```sh
open week11/lab/reports/ollama-report.html
```

### 08. 실제 LLM 평가와 실행 추적

[08_ollama_judge_and_traces.ipynb](notebooks/08_ollama_judge_and_traces.ipynb)

07번과 같은 Ollama 준비가 필요하며, 07번 변수를 요구하지 않습니다.

1. J01·J02·J03·J05를 **실제 모델**에 전달합니다. `actual`과 `reason`은 새 응답입니다.
2. 참고 판정과 실제 판정이 일치한 수를 확인하고, 불일치 행의 이유를 읽습니다. 05번의 62.5%와 같을 필요가 없습니다.
3. Q03a를 새로 생성하고 평가합니다. 생성 답변, 기계적 검사, LLM 판정을 따로 확인합니다.
4. `trace_id`와 `spans` 표에서 검색·생성·코드 검사·LLM 평가가 같은 요청에 연결되는지 확인합니다.
5. Langfuse·LangSmith의 trace/dataset/experiment/score 용어와 로컬 기록의 관계를 확인합니다.
6. `reports/judge/ollama-report.html`을 열어 실제 판정과 근거를 확인합니다.

같은 작은 모델의 자기 평가는 독립적인 정확성 보증이 아닙니다. 선택 사례 4건의 일치율도 일반적인 모델 성능이 아닙니다. 실제 계정 연동 없이 로컬 기록으로 마치며, 이 JSONL을 제품에 직접 업로드할 수 있는 전송 포맷으로 소개하지 않습니다.

**기본 속도 설정:** 1.5B instruct, 문맥 2,048토큰, 출력 상한 192토큰(평가 128), temperature=0, seed=11, 모델 유지 10분. thinking 지원 모델로 바꾸면 `think=False`를 보냅니다. 최초 로딩이나 다른 프로세스에 따라 지연은 달라집니다.

## 3. 빠른 사전 점검과 재검증

```sh
python -m week11.lab.run_eval
python -m pip install -r requirements/dev.txt
python -m pytest week11/lab/tests -q
```

2026-11-11 재확인: Notebook 8개·코드 셀 56개 오류 0, 테스트 29개 통과, `pip check` 통과. 01–06의 검색 평가 결과 JSON은 공개 샘플과 전체 일치했습니다. 07–08의 실제 생성 문장·지연·추적 ID는 실행마다 달라질 수 있습니다. 검증 환경은 macOS arm64 / Python 3.11.14입니다.

- [실제 Ollama 실행 예제](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/ollama/ollama-report.html)
- [브라우저용 예제 보고서](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/report.html): 설치 전 미리 확인
- 직접 실행한 `reports/`: 로컬 결과, Git 제외, 공개 페이지에 자동 업로드되지 않음
- 실행 중 빨간 오류: 커널 경로와 첫 환경 셀부터 확인. 변수 순서가 섞였으면 **Restart Kernel → Run All**

## 4. 실제 Langfuse 연결과 심화 실험

09–10은 **추가 설치와 Docker 기동**이 필요합니다. 기존 01–08과 독립적으로 실행할 수 있습니다. [한 번만 수행하는 준비 명령·로그인](langfuse/README.md#수업-전-준비-설치-대기는-수업-시간-밖으로)을 먼저 완료합니다.

### 09. 실제 요청 추적 · 수업 핵심 20분

[09_langfuse_ollama_tracing.ipynb](notebooks/09_langfuse_ollama_tracing.ipynb)

1. 첫 셀: 로컬 인증·Ollama 버전 확인. 비밀번호·키는 출력하지 않습니다.
2. 1단계: 최소 SDK 구문의 실제 생성. trace 아래 generation 하나와 실제 입출력 확인.
3. **2단계:** Q03a의 전체 요청 실행. 교환 기간·비용·조건을 확인.
4. **3단계:** 서버 재조회. 부모 1개와 하위 작업 4개의 연결 확인.
5. **4단계:** Scores의 코드 검사와 모델 판정을 구분하고 참고 기준 대조.
6. **5단계:** Q24a 재고 질문의 baseline/grounded 비교. 모르는 상태와 재고 없음의 차이 확인.
7. 6단계: 답변을 직접 읽은 뒤 사람 검토 입력. 기본 None은 미실행이며 가짜 사람 점수를 만들지 않습니다.
8. 7–8단계: 로컬 결과 저장, 다음 실험 가설 정리.

수업에서는 굵게 표시한 2–5단계를 중심으로 진행합니다. 총 모델 호출 7회는 전체 실행 기준이며, 문장·judge 판정·지연은 실행마다 달라질 수 있습니다.

### 10. 같은 데이터의 실험과 배포 전 검증 · 수업 핵심 25분

[10_langfuse_experiments_release_gate.ipynb](notebooks/10_langfuse_experiments_release_gate.ipynb)

| 단계 | 실행 | 확인 결과 |
|---|---|---|
| 1 | 재고 질문의 실제 요청 | 출처 trace와 개선 가설 |
| 2 | 정상 3건 + 경계 1건 데이터 | Datasets의 입력·참고 기준·기능 유형 |
| 3 | A 기존 프롬프트 | 4개 실제 실행과 평가 |
| 4 | B 근거 제한 프롬프트 | 같은 데이터의 실제 변경 효과 |
| 5 | C 기능 정책 | 정상 상담은 실제 모델 호출, 미지원 조회는 정책 응답 |
| 6 | 필수 조건과 사람 검토 | HOLD 또는 REVIEW; 자동 배포 아님 |
| 7 | 서버 재조회 | 실험 3개 × 요청 4개의 저장 확인 |
| 8 | 보고서 저장 | reports/langfuse/release-comparison.json |

기본 전체 실행에서 실제 모델 호출은 24회입니다. C의 재고 경로는 모델 생성·평가를 하지 않고 서비스가 기권 응답을 반환하므로 `not_run`으로 표시합니다. 기능 유형은 UI 메뉴/API 라우트 입력이며, 참고 정답으로 분기하지 않습니다.

검증된 수업 사례에서는 A/B의 인용·기권 검사 통과율이 75%, C는 100%였고 B는 HOLD, C는 REVIEW였습니다. 이는 **4건의 계약 검사 결과**이며 답변 의미 정확도나 실제 운영 승인으로 해석하지 않습니다. [실제 결과 미리 보기](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/langfuse/)에서 답변과 판정을 직접 비교할 수 있습니다.


## 교수·학생용 화면 바로가기

[화면별 시연 안내](https://smilesjcha.github.io/llmops-16week/week11/lab/demo/)에는 클릭 위치, 질문, 확인 결과, 설명 포인트와 시간을 정리했습니다.
09·10의 마지막 기록 저장 셀을 실행한 후 `python -m week11.lab.demo_guide`를 실행하면 `week11/lab/reports/langfuse/instructor-console.html`에 이번 실행의 실제 trace·비교 URL이 들어갑니다. 브라우저로 열어 사용합니다. 실행 결과와 안내 파일은 Git 제외입니다.


## 09·10 한 셀씩 실행하는 순서

[코드 셀별 실행표](https://smilesjcha.github.io/llmops-16week/week11/lab/demo/#notebooks)와 각 Notebook 첫 설명을 참고합니다. 번호는 **설명 셀을 제외하고 위에서부터 세는 코드 셀 순서**입니다. VS Code의 `[1]`, `[2]`는 실행 횟수이므로 셀 번호로 사용하지 않습니다.

- 09: 환경 → 최소 생성 → 전체 요청 → 서버 저장 → 점수 → 재고 비교 → 사람 검토 → 저장 → 개선 정리.
- 10: 환경 → 경계 요청 → 고정 데이터 → A → B → C → 비교 → 서버 저장 확인 → 결과 저장.
- 각 셀의 완료 후 다음 셀로 이동합니다. 10번 첫 환경 셀도 다시 실행합니다.
- 같은 실험이 여러 번 쌓였다면 현재 Notebook 출력의 링크를 사용합니다. 데이터의 source trace는 해당 데이터가 처음 만들어진 요청일 수 있습니다.
