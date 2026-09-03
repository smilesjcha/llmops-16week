# Week 01 — Orientation & LLM Lifecycle

첫 주의 목표는 LLM을 한 번 호출하는 것이 아니라, 한 번의 실행을 기록·비교·개선 가능한 서비스로 바꾸는 것이다.

## 구성

- `lecture/01_week1_강의안.md`: 79장 강의 콘티, 180분/100분 운영 경로, 교수자 노트
- `lecture/PPT_PRODUCTION_GUIDELINE.md`: 16주 공통 PPT 제작·검수 기준
- `lecture/DESIGN_SYSTEM.md`: black / white / navy / blue 기반 Week 01 시각 시스템
- `lecture/01_week1_llmops_kickoff.pptx`: 79장 실제 강의용 슬라이드
- `lab/`: offline-first FastAPI 서비스 `TRACE/01`
- `lab/week01_trace01_lab.ipynb`: 실행·trace·비교·개선 guided lab
- `TEST_REPORT.md`: 의존성·코드·PPTX 검증 결과와 수동 검사 경계

PPT는 과정별 60–80장 범위에서 구성한다. Week 01은 79장이며, 모든 제목·부제는 명사형을 기본값으로 한다. 화면에 보이는 글자는 14pt 이상, 본문은 18pt 이상을 유지하고, 주황색 없이 검정·흰색·네이비·파랑 계열만 사용한다. 파란색은 마지막 위치가 아니라 현재 변수·운영 증거·판정 상태처럼 맥락상 필요한 요소에만 적용하며, 동일 레이아웃은 세 장 연속 사용하지 않는다.

## 실습 바로 시작

```bash
uv python install 3.11.14
uv venv --python 3.11.14 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --app-dir week01/lab --reload
```

브라우저에서 <http://127.0.0.1:8000>을 열고 같은 입력으로 두 번 실행한 뒤 trace를 비교한다. 자세한 순서는 [lab README](lab/README.md)를 따른다.
