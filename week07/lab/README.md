# Week 07 · 단계별 모델 적응·기획 실습

모델 다운로드·API 키·Ollama·GPU 없이 실행하는 공통 경로다. Python 3.11, NumPy 1.26.4와 기존 Jupyter 환경을 사용한다. 공통 `requirements.txt`에 패키지를 추가하지 않았다.

## VS Code 실행

저장소 루트를 열고 터미널에서:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
code .
```

이미 `.venv`가 있으면 재생성하지 말고 활성화부터 진행한다. Windows 활성화는 `.venv\Scripts\activate`다. VS Code Python·Jupyter 확장 설치 후 Notebook 오른쪽 **Select Kernel → Python Environments → .venv / Python 3.11**을 선택한다. 시스템 Python이나 별도 가상환경을 섞지 않는다.

## 순서와 학습 내용

| 순서 | Notebook | 핵심 실험 | 권장 시간 |
|---|---|---|---:|
| 01 | [데이터 품질·분할](notebooks/01_data_quality_split.ipynb) | 48건 검사, 중복·깨진 JSON, 문장/사건 분할, 누출 탐지, Dataset Card | 15분 |
| 02 | [저차원 행렬](notebooks/02_low_rank_adaptation.ipynb) | rank 1·2·4·8, 근사 오차·파라미터, scaling, 원본 고정 | 10분 |
| 03 | [선호 데이터·DPO](notebooks/03_preference_dpo.ipynb) | 선호쌍 검토, reference 대비 손실, beta, 단일 질문 정책 최적화 | 15분 |
| 04 | [기획서 초안](notebooks/04_project_proposal.ipynb) | 대안·평가·위험·역할, 누락 검사, HTML/JSON, 피드백 기록 | 15분 |

총 110셀 / 코드 53셀. 위에서 아래로 실행한다. 35분 수업 실습에서는 01의 분할·누출 셀, 02의 rank·오차 셀, 03의 손실·정책 셀, 04의 문서 생성 셀을 우선하고 나머지는 확장 실험으로 진행한다. 04는 앞 노트북의 산출물이 없어도 실행되며 미실행 상태를 표시한다.

## 결과 확인

출력은 Git 추적에서 제외된 `output/validation/adaptation-labs/`다.

- `dataset-card.json`: 48건, train32 / dev8 / test8, seed42
- `low-rank-report.json`: 행렬 근사 오차와 파라미터 수
- `preference-report.json`: 장난감 정책 결과와 실제 모델 평가 계획
- `proposal-draft.html`: 브라우저로 열고 검토할 기획서 시안
- `proposal-draft.json`, `feedback-log.json`: 기획 항목과 피드백 기록

HTML을 VS Code에서 **Reveal in Finder/Explorer**로 찾아 브라우저에서 연다. 필요하면 브라우저 인쇄 → PDF 저장을 이용한다. 예시를 자신의 문제로 바꾸고 근거·권한·평가 계획을 직접 검토한 뒤 제출한다. 자동 항목 검사 통과는 교수 평가 통과가 아니다.

## 실험의 경계

- SVD는 이미 만든 행렬의 근사다. 실제 LoRA Adapter를 학습하지 않는다.
- DPO 예시는 질문 하나와 고정 답변 두 개의 Bernoulli policy를 학습한다. 언어 모델이나 새 질문의 일반화를 검증하지 않는다.
- 문자 길이를 토큰 길이로 해석하지 않는다.
- HTML은 기획 문서 시안이다. 서비스 프로토타입 구현이 아니다.
- 실제 SFT/DPO 학습은 `AS-IS 2025 2nd semester/practice/week06/`, `week07/` 보존본을 별도 GPU 환경에서 재검증한 후 선택한다. `requirements/finetune-week06-07.txt`는 legacy 후보이며 공통 .venv에 섞어 설치하지 않는다.

## 재검증

```bash
python -m pytest -q course_labs/tests/test_adaptation.py
python scripts/verify_adaptation_notebooks.py
```

4개 노트북은 독립 커널에서 실행 검증했다. 개인정보와 학생 원문은 공개 저장소에 넣지 않는다.
