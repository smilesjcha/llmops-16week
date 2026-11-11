# 11주차 실습: 평가 데이터부터 배포 전 판단까지

기존 Python 3.11 환경에서 실행합니다. **Ollama·Docker·GPU·API 키는 필요 없습니다.** 인터넷은 최초 패키지 설치에만 필요합니다. 직접 실행해 비교하고 실패 원인을 설명하는 실습입니다.

- [11주차 HTML 강의안 바로 보기](https://smilesjcha.github.io/llmops-16week/week11/lecture/)
- [실습 평가 보고서 바로 보기](https://smilesjcha.github.io/llmops-16week/week11/lab/sample/report.html): 설치·다운로드 없이 필터와 근거 탐색을 먼저 체험할 수 있습니다.

공개 보고서는 수업용 합성 데이터로 실행한 예제입니다. 아래 명령으로 직접 실행한 결과는 자신의 `week11/lab/reports/report.html`에 저장되며 공개 페이지에 자동 업로드되지 않습니다.

## VS Code 준비

1. 저장소를 받거나 기존 저장소를 최신 상태로 갱신합니다. 개인 수정이 있으면 먼저 보관하고, git pull --ff-only가 실패하면 강제로 덮어쓰지 않습니다.

    git clone https://github.com/smilesjcha/llmops-16week.git
    cd llmops-16week

2. VS Code에서 llmops-16week **폴더 전체**를 엽니다. Python과 Jupyter 확장을 설치합니다.
3. 기존 .venv가 있으면 재사용합니다. 없으면 Python 3.11로 만듭니다.

macOS / Linux:

    python3.11 -m venv .venv
    source .venv/bin/activate

Windows PowerShell:

    py -3.11 -m venv .venv
    .\.venv\Scripts\Activate.ps1

PowerShell 활성화가 제한된 환경에서는 정책을 바꾸지 않고 아래 명령의 python 대신 .\.venv\Scripts\python.exe를 사용합니다.

4. 터미널에서 설치하고 버전을 확인합니다.

    python --version
    python -m pip install -r requirements/week11-offline.txt
    python -m pip check

예상 Python 버전은 3.11.x입니다. 공통 base에 scikit-learn 및 과학 계산 의존성을 추가한 전용 프로필입니다. 기존 16주 공통 requirements를 덮어쓰지 않습니다. 이 배포의 실제 검증 환경은 macOS arm64 / Python 3.11.14이며 다른 운영체제의 실기 검증을 했다고 주장하지 않습니다.

## 가장 빠른 사전 점검

저장소 루트에서 실행합니다.

    python -m week11.lab.run_eval

생성되는 파일:

- reports/report.html: 브라우저로 열어 필터·질문 검색·근거 보기
- reports/results.json: 설정·데이터 해시·지표·문항별 결과·판단

VS Code 탐색기에서 report.html을 찾아 운영체제의 파일 탐색기에 표시한 뒤 브라우저로 열거나, macOS 터미널에서는 아래처럼 엽니다.

    open week11/lab/reports/report.html

정상 결과는 **HOLD**입니다. 후보가 일부 기준을 충족하지 못했다는 의미입니다. CLI 기본 실행은 결과를 생성한 뒤 종료 코드 0으로 끝납니다.

자동 차단을 실험할 때만 사용:

    python -m week11.lab.run_eval --enforce-gate

HOLD이면 종료 코드 2입니다. 이것을 설치 오류로 오해하지 마세요. REVIEW로 바뀌더라도 사람 검토와 온라인 검증이 필요하며 자동 배포 명령은 없습니다.

## Notebook 실행 순서

각 파일을 열어 오른쪽 위 **Select Kernel → Python Environments → 저장소 .venv**를 선택합니다. 독립 실행이 가능하며 다른 Notebook을 미리 실행할 필요는 없습니다. 각 파일에는 목적·코드·확인 결과·확장 실험·문제 해결 안내가 있습니다.

| 순서 | 파일 | 핵심 실행 / 배울 내용 |
|---|---|---|
| 01 | [데이터 계약](notebooks/01_dataset_contract.ipynb) | 문서·질문 구조, 유형 분포, 잘못된 gold, 그룹 누수 |
| 02 | [검색 기준선](notebooks/02_retrieval_baselines.ipynb) | 단어/문자 TF-IDF, 띄어쓰기, 빈 검색, 버전 필터, 동점 |
| 03 | [지표와 k](notebooks/03_metrics_and_k.ipynb) | Hit/Recall 차이, MRR/nDCG 손계산, 독립 구현 대조, 분모 |
| 04 | [기권과 오류](notebooks/04_calibration_and_error_analysis.ipynb) | dev 선택, 임계값 곡선, 고정 test, 말투별 실패 추적 |
| 05 | [평가자 검증](notebooks/05_judge_rubric.ipynb) | 수업용 루브릭, JSON 계약, 불일치 행렬, 순서 편향 |
| 06 | [보고서와 판단](notebooks/06_release_report.ipynb) | 재현 실행, 그룹 bootstrap, 검증 조건, 독립 HTML 보고서 |

총 126셀, 코드 42셀입니다. 수업에서는 각 파일의 핵심 단계부터 실행하고 확장 항목은 복습합니다. 모든 파일은 새 커널에서 Run All로 검증했습니다.

### 학생이 직접 바꿀 부분

- 01: 새 의도의 질문·필수 문서·답변 가능 여부 추가
- 02: analyzer 또는 current_only 중 하나씩 변경
- 03: k=1,3,5로 비교하고 서비스 성공 조건 정의
- 04: dev에서 임계값과 목적함수 검토, test 실패 근거 기록
- 05: 조건 누락·수치 충돌·잘못된 전제 fixture 추가
- 06: 실제 프로젝트의 위험·비용에 맞는 판단 기준 제안

test를 반복 관찰하며 설정을 바꾸면 새 평가 세트가 필요합니다. 공개 학습용 test를 실제 미공개 서비스 성능의 근거로 쓰지 않습니다.

## 코드 구조와 정의

- evaluation.py: 입력 검증, 검색, 지표, dev 선택, bootstrap, 판단
- judging.py: 작성 fixture와 평가 JSON 검증. 모델 호출 없음
- run_eval.py: 명령행 실행과 보고서 저장
- report-template.html: 결과를 내장하는 HTML 탐색기
- data/: 22개 가상 문서와 48개 교수 작성 질문
- sample/: 배포 시 실제 실행한 합성 자료 보고서
- reports/: 학생의 로컬 실행 결과. Git 제외

**검색 지표**는 기권 전의 순위 품질이고 답변 가능 문항만 평균냅니다.
**필수 근거 확보율**은 답변 가능한 질문 중 수락했고 모든 gold 문서를 찾은 비율입니다.
**답변 불가 수락률**의 분모는 답변 불가 질문, **응답 시도 비율**의 분모는 전체 질문입니다.
어느 것도 생성된 답변의 정확성 자체를 측정하지 않습니다.

## 오류 해결

| 증상 | 확인 및 해결 |
|---|---|
| sklearn / pandas 없음 | 선택한 커널과 설치 터미널이 같은 .venv인지 확인 |
| Python 3.11 안내 | VS Code 커널을 저장소 Python 3.11 환경으로 변경 |
| 저장소 경로 오류 | 폴더 전체를 열고 그 안의 Notebook에서 실행 |
| pytest 없음 | python -m pip install -r requirements/dev.txt |
| reports 파일 없음 | 저장소 루트에서 python -m week11.lab.run_eval |
| HTML이 코드로 보임 | 위의 GitHub Pages 바로 보기 링크 이용. 자신의 실행 결과는 로컬 report.html을 브라우저로 열기 |
| 빈 필터 결과 | 필터 초기화 / 입력 검색어 지우기 |
| --enforce-gate 종료 2 | HOLD의 의도된 차단. report.html에서 실패 조건 확인 |

검증:

    python -m pip install -r requirements/dev.txt
    python -m pytest week11/lab/tests -q

## 프로젝트 적용 기록

결론 → 조건과 버전 → 지표와 실패 사례 → 한계 → 다음 실험 순서로 정리합니다.
원문·고객 정보·API 키·학생 제출물은 공개 GitHub에 올리지 않습니다.
실제 API/임베딩/LLM judge는 선택 확장이며 기본 검증 범위에 포함되지 않습니다.
