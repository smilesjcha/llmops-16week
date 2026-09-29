# Week 04 · 단계별 실습

## VS Code 준비

저장소 **루트 폴더**를 VS Code로 연다. Python·Jupyter 확장을 설치하고 터미널에서 실행한다.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m pytest -q course_labs/tests
```

이미 `.venv`가 있으면 생성은 생략한다. Windows는 `py -3.11 -m venv .venv`,
PowerShell 활성화는 `.venv\Scripts\Activate.ps1`이다. 보안 정책을 변경하지 말고 필요하면
`.venv\Scripts\python.exe -m pip install -r requirements.txt`처럼 직접 실행한다.
검증 기준 CPython 3.11.14, 지원 minor 3.11. 패키지 버전은 루트 requirements의 고정값을 따른다.

## Notebook 실행 순서

오른쪽 위 **Select Kernel → Python Environments → .venv**를 선택한다.
첫 셀에서 Python 버전과 저장소 경로를 확인하고 위에서 아래로 `Shift+Enter`로 실행한다.
설정을 바꿨으면 해당 셀과 그 결과를 사용하는 다음 셀을 다시 실행한다.
마무리는 **Restart Kernel → Run All**로 숨은 실행 순서 의존성을 확인한다.

| 순서 | Notebook | 직접 해보는 작업 |
|---|---|---|
| 01 | [문서·분할](notebooks/01_documents_chunking.ipynb) | 출처·버전 표, 문자 위치, 겹침, 메타데이터, 날짜·접근 필터 |
| 02 | [검색·근거](notebooks/02_retrieval_evidence.ipynb) | 검색 순위, 동의어 실패, 문서 수, 출처, 발췌·답변 보류 |
| 03 | [평가·실패](notebooks/03_evaluation_failures.ipynb) | Recall·MRR 직접 계산, 개발/테스트 분리, 없는 답, 예외·API 검증 |
| 04 | [선택 Ollama](notebooks/04_optional_ollama.ipynb) | 실제 임베딩·코사인 검색·LLM 답변, thinking 끄기, 모델 연결 오류 |

각 notebook은 34셀(코드 12셀)이다. 예측 → 실행 → 설정 하나 변경 → 차이 설명 → 미니 과제로 이어진다.
기본 실습 01–03은 API 키·모델 다운로드 없이 실행한다. 04도 기본 Run All은 외부 호출 없이 통과하며,
실제 모델을 사용하려면 설치·모델 준비 후 해당 셀의 `RUN_*` 스위치를 직접 켠다.

## 서비스 화면

```bash
python -m uvicorn week04.lab.rag04.main:app --host 127.0.0.1 --port 8004
```

브라우저 `http://127.0.0.1:8004`에서 질문을 바꾼다. `상품 반품 기간`, `돈은 언제 돌려줘요`,
`화성 우주 정거장 운임`, `내부 승인 티켓 EX-77`을 비교한다. 날짜·역할·동의어를 하나씩 바꾸고
16개 질의 평가 → JSON 저장을 실행한다. 종료는 터미널 `Ctrl+C`.

평가는 질의 파일에 지정된 역할·기준 날짜를 고정한다. 화면의 날짜·역할 변경은 **개별 검색**에 적용된다.

Ollama 503은 앱 성공이 아니다. `ollama serve`, `ollama list`, 모델 이름, 포트11434 연결을 확인한다.
Qwen3은 요청의 `think: false`로 사고 출력을 끈다. 생성 토큰 수도 제한한다. 하드웨어별 속도는 다르며
기본 로컬 실습에는 Ollama가 필요 없다.

## 해석과 한계

- TF-IDF는 단어 통계 기반 벡터이며 학습된 의미 임베딩이 아니다.
- 토큰화는 수업용 단어·한글 n-gram이며 형태소 분석기가 아니다.
- 기본 응답은 첫 근거의 원문 발췌. 다중 근거 종합이나 LLM 생성 품질을 측정하지 않는다.
- 접근 역할 선택은 모의 실험이며 실제 인증·권한 통제가 아니다. 서버를 외부에 공개하지 않는다.
- 현재·미래 문서 적용 구간이 겹치는 데이터는 충돌 탐지 실험용이다. 무조건 최신 버전 선택으로 숨기지 않는다.
- `answerable_abstention`은 답이 있는 질의에서도 보류한 비율이다. `correct_abstention`만으로 서비스 품질을 판단하지 않는다.
